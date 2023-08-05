import fnmatch
import re
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from functools import partial
from threading import RLock
from string import Formatter
import os
import hashlib
import sys
from fasteners import lock, process_lock
import errno
import json


if sys.version_info[0] == 3:
    read_input = input
else:
    read_input = raw_input

try:
    from inspect import getattr_static
    getattr_safe = getattr_static
except:
    getattr_safe = getattr


locked = lock.locked


def is_str(s):
    try:
        return type(s) == str or type(s) == unicode
    except NameError:
        return type(s) == str

def decode_str(s):
    try:
        return s.decode()
    except:
        return s

def decorate_append(func, extra_func):
    def _f(*args, **kwargs):
        val = func(*args, **kwargs)
        extra_func(*args, **kwargs)
        return val
    return _f

def decorate_prepend(func, extra_func):
    def _f(*args, **kwargs):
        extra_func(*args, **kwargs)
        return func(*args, **kwargs)
    return _f

def as_list(t):
    return [t] if type(t) == str else list(t)

def as_stable_string_list(o):
    if type(o) == list or type(o) == tuple:
        return sorted([str(item) for item in o])
    elif type(o) == dict:
        return sorted(["{0}={1}".format(key, as_stable_string_list(val))
                       for key, val in o.items()])
    else:
        return [str(o)]

def as_stable_tuple_list(o):
    assert type(o) == dict, "as_stable_tuple_list: argument is not a dict"
    l = [(key, value) for key, value in o.items()]
    return sorted(l, key=lambda x: x[0])

def as_human_size(size):
    unit_precision = [("B", 0), ("KB", 0), ("MB", 1), ("GB", 2), ("TB", 2), ("PB", 2)]
    index = 0
    while size > 1024:
        size /= 1024
        index += 1
    return "{0} {1}".format(round(size, ndigits=unit_precision[index][1]), unit_precision[index][0])

def as_dirpath(dirpath):
    return dirpath + os.path.sep if dirpath[-1] != os.path.sep else dirpath

def call_or_return(obj, t):
    return t(obj) if callable(t) else t

def call_or_return_list(obj, t):
    return as_list(call_or_return(obj, t))

def call_and_catch(f, *args, **kwargs):
    try:
        return f(*args, **kwargs)
    except KeyboardInterrupt as e:
        raise e
    except:
        return None

def call_and_catch_and_log(f, *args, **kwargs):
    try:
        return f(*args, **kwargs)
    except KeyboardInterrupt as e:
        raise e
    except:
        from jolt import log
        log.exception()
        return None

def parse_task_name(name):
    if ":" in name:
        task, params = name.split(":", 1)
        params = params.split(",")
        def _param(param):
            if "=" in param:
                key, value = param.split("=", 1)
            else:
                key, value = param, None
            return key, value
        return task, {key: value for key, value in map(_param, params) if key}
    else:
        return name, {}

def format_task_name(name, params):
    if not params:
        return name
    def _param(key, value):
        return "{0}={1}".format(key, value) if value is not None else key
    params = sorted([(key, value) for key, value in params.items()], key=lambda x: x[0])
    return "{0}:{1}".format(name, ",".join([_param(key, value) for key, value in params]))

def stable_task_name(name):
    task, params = parse_task_name(name)
    return format_task_name(task, params)

def canonical(s):
    return "".join([c if c.isalnum() else '_' for c in s])


def unique_list(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]


def pathmatch(string, pattern):
    pattern = fnmatch.translate(pattern)
    pattern = pattern.replace('(?s:.*.*/', '(?s:(^|.*/)')
    pattern = pattern.replace('/.*.*/', '.*/')
    return re.compile(pattern).match(string)


def quote_path(string):
    return '"' + string + '"' if ' ' in string else string


class _SafeDict(object):
    def __init__(self, values, ignore_errors=False):
        self.values = values
        self.errors = not ignore_errors

    def _envget(self, key):
        if key.startswith("ENV|"):
            return os.environ.get(key[4:])
        return None

    def __getitem__(self, key):
        value = self.values.get(key)
        if value is None:
            value = call_and_catch(getattr, self.values.get("_instance", object()), key)
        if value is None:
            value = self._envget(key)
        if value is not None:
            return value
        if self.errors:
            raise KeyError(key)
        return "{" + key + "}"


def expand(string, *args, **kwargs):
    ignore_errors = kwargs.get("ignore_errors") or False
    return Formatter().vformat(str(string), args, _SafeDict(kwargs, ignore_errors))


class duration(object):
    def __init__(self):
        self._time = time.time()

    def __str__(self):
        elapsed = self.seconds
        if elapsed >= 3600:
            return time.strftime("%Hh %Mmin %Ss", time.gmtime(elapsed))
        if elapsed >= 60:
            return time.strftime("%Mmin %Ss", time.gmtime(elapsed))
        return time.strftime("%Ss", time.gmtime(elapsed))

    def __le__(self, d):
        now = time.time()
        elapsed1 = now - self._time
        elapsed2 = now - d._time
        return elapsed1 < elapsed2

    def __sub__(self, delta):
        assert type(delta) in [int, float]
        self._time -= int(delta+.5)
        return self

    def diff(self, d):
        if d is None:
            return duration_diff(0)
        now = time.time()
        elapsed1 = now - self._time
        elapsed2 = now - d._time
        return duration_diff(abs(elapsed1 - elapsed2))

    @property
    def seconds(self):
        return time.time() - self._time

    @property
    def milliseconds(self):
        return (time.time() - self._time) * 1000

class duration_diff(object):
    def __init__(self, elapsed):
        self._elapsed = elapsed

    def __str__(self):
        elapsed = self._elapsed + 0.5
        if elapsed <= 1:
            return ""
        if elapsed >= 3600:
            return time.strftime("[%Hh %Mmin %Ss] ", time.gmtime(elapsed))
        if elapsed >= 60:
            return time.strftime("[%Mmin %Ss] ", time.gmtime(elapsed))
        return time.strftime("[%Ss] ", time.gmtime(elapsed))

    def __iadd__(self, dur):
        if isinstance(dur, duration):
            now = duration()
            self._elapsed += dur.diff(now)._elapsed
        if type(dur) == int:
            self._elapsed += dur
        return self

    @property
    def elapsed(self):
        return self._elapsed


class cached:
    mutex = RLock()

    @staticmethod
    def instance(f):
        def _f(self, *args, **kwargs):
            attr = "__cached_result_" + str(id(f))
            with cached.mutex:
                if not hasattr(self, attr):
                    setattr(self, attr, f(self, *args, **kwargs))
            return getattr(self, attr)
        return _f

    @staticmethod
    def method(f):
        def _f(*args, **kwargs):
            attr = "__cached_result_" + str(id(f))
            with cached.mutex:
                if not hasattr(f, attr):
                    setattr(f, attr, f(*args, **kwargs))
            return getattr(f, attr)
        return _f


class retried:
    @staticmethod
    def on_exception(exc_type, pattern=None, count=8, backoff=[1,4,10,15,20,25,35,40]):
        def _decorate(f):
            def _f(*args, **kwargs):
                for i in range(0, count):
                    try:
                        if i > 0:
                            time.sleep(backoff[i - 1])
                        return f(*args, **kwargs)
                    except exc_type as e:
                        if i+1 >= count:
                            raise e
                        if pattern is None or pattern in str(e):
                            from jolt import log
                            log.debug("Exception caught, retrying : " + str(e))
                            continue
            return _f
        return _decorate


def Singleton(cls):
    cls._instance = None
    @staticmethod
    def get(*args, **kwargs):
        if not cls._instance:
            cls._instance = cls(*args, **kwargs)
        return cls._instance
    cls.get = get
    return cls


class LockFile(object):
    def __init__(self, path, logfunc=None, *args, **kwargs):
        self._file = process_lock.InterProcessLock(os.path.join(path, "lock"))
        if not self._file.acquire(blocking=False):
            if logfunc is not None:
                logfunc(*args, **kwargs)
            self._file.acquire()

    def __enter__(self, *args, **kwargs):
        return self

    def __exit__(self, *args, **kwargs):
        pass


def map_consecutive(method, iterable):
    return list(map(method, iterable))

def map_concurrent(method, iterable, *args, **kwargs):
    max_workers = kwargs.get("max_workers", None)
    callables = [partial(method, item) for item in iterable]
    futures = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for call in callables:
            futures.append(executor.submit(call))
        for future in as_completed(futures):
            try:
                future.result()
            except Exception:
                for future in futures:
                    future.cancel()
    return [future.result() for future in futures]


def sha1(string):
    sha = hashlib.sha1()
    sha.update(string.encode())
    return sha.hexdigest()


def filesha1(path):
    sha = hashlib.sha1()
    with open(path, "rb") as f:
        for data in iter(lambda: f.read(0x10000), b''):
            sha.update(data)
    return sha.hexdigest()


def fromjson(filepath, ignore_errors=False):
    try:
        with open(filepath) as f:
            return json.loads(f.read())
    except Exception as e:
        if ignore_errors:
            return {}
        raise e


def tojson(filepath, data, ignore_errors=False, indent=2):
    try:
        with open(filepath, "w") as f:
            f.write(json.dumps(data, indent=indent))
    except Exception as e:
        if ignore_errors:
            return
        raise e


def concat_attributes(attrib, postfix, prepend=False):
    def _decorate(cls):
        _orig = getattr(cls, "_" + attrib)
        def _get(self):
            orig = _orig(self)
            if prepend:
                return getattr(self, self.expand(postfix), type(orig)()) + orig
            else:
                return orig + getattr(self, self.expand(postfix), type(orig)())
        setattr(cls, "_" + attrib, _get)
        return cls
    return _decorate
