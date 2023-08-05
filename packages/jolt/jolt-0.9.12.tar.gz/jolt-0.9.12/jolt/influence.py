import datetime
import hashlib
import os
import uuid
from pathlib import Path, PurePath

from jolt import utils
from jolt import log
from jolt import filesystem as fs
from jolt import tools


_providers = []

@utils.Singleton
class HashInfluenceRegistry(object):
    @staticmethod
    def Register(cls):
        _providers.append(cls)

    def __init__(self):
        self._providers = [provider() for provider in _providers]

    def register(self, provider):
        self._providers.append(provider)

    def apply_all(self, task, sha):
        for influence in self.get_strings(task):
            sha.update(influence.encode())
            #log.debug("{0}: {1}", task.name, influence)

    def get_strings(self, task):
        content = []
        for provider in self._providers + task.influence:
            for line in str(provider.get_influence(task)).splitlines():
                content.append("Influence-{0}: {1}".format(provider.name, line))
        return content


class HashInfluenceProvider(object):
    name = "X"
    def get_influence(self, task):
        raise NotImplemented()


class TaintInfluenceProvider(object):
    name = "Taint"

    def get_influence(self, task):
        return str(task.taint)


class TaskAttributeInfluence(HashInfluenceProvider):
    def __init__(self, attrib, sort=False):
        self._attrib = attrib
        self._sort = sort
        self.name = attrib.title()

    def get_influence(self, task):
        value = getattr(task, tools.Tools(task).expand(self._attrib), "N/A")
        try:
            value = value.__get__(task)
            if type(value) == list and self._sort:
                value.sort()
        except AttributeError:
            pass
        return value


def attribute(name, sort=False):
    """ Add task attribute value as hash influence.

    Args:
        name (str): Name of task class attribute/property.

    Example:

    .. code-block:: python

        from jolt import influence

        @influence.source("attribute")
        class Example(Task):
            attribute = False
    """

    def _decorate(cls):
        _old_influence = cls._influence
        def _influence(self, *args, **kwargs):
            influence = _old_influence(self, *args, **kwargs)
            influence.append(TaskAttributeInfluence(name, sort))
            return influence
        cls._influence = _influence
        return cls
    return _decorate


class TaskSourceInfluence(HashInfluenceProvider):
    def __init__(self, funcname, obj=None):
        self.name = "Source"
        self.funcname = funcname
        self.obj = obj

    @staticmethod
    def _default_func():
        pass

    def get_influence(self, task):
        obj = self.obj or task
        try:
            funcname = self.funcname
            funcname = obj.expand(funcname)
        except:
            pass

        # Collect all functions from the class hierarchy
        if type(obj) == type:
            funcs = [utils.getattr_safe(mro, funcname, TaskSourceInfluence._default_func)
                     for mro in obj.mro()]
        else:
            funcs = [utils.getattr_safe(mro, funcname, TaskSourceInfluence._default_func)
                     for mro in obj.__class__.mro()]

        # Calculate sha1 sum for all functions
        shasum = hashlib.sha1()
        for func in funcs:
            try:
                func.__influence
            except AttributeError:
                func.__influence = utils.sha1(task._get_source(func))
            finally:
                shasum.update(func.__influence.encode())

        return shasum.hexdigest() + ": " + funcname


def source(name, obj=None):
    """ Add function source code as hash influence.

    Args:
        name (str): Name of function in task class.

    Example:

    .. code-block:: python

        from jolt import influence

        @influence.source("method")
        class Example(Task):
            def method(self):
                return False

    """
    def _decorate(cls):
        _old_influence = cls._influence
        def _influence(self, *args, **kwargs):
            influence = _old_influence(self, *args, **kwargs)
            influence.append(TaskSourceInfluence(name, obj))
            return influence
        cls._influence = _influence
        return cls
    return _decorate


class TaskRequirementInfluence(HashInfluenceProvider):
    name = "Requirement"

    def __init__(self, proxy):
        self._identity = proxy.identity
        self._name = proxy.short_qualified_name

    def get_influence(self, task):
        return "{}: {}".format(self._identity,self._name)


@HashInfluenceRegistry.Register
class TaskNameInfluence(HashInfluenceProvider):
    name = "Name"
    def get_influence(self, task):
        return task.name


@HashInfluenceRegistry.Register
class TaskParameterInfluence(HashInfluenceProvider):
    name = "Parameters"
    def get_influence(self, task):
        return ",".join(
            sorted(["{0}={1}".format(key, value)
                    for key, value in task._get_parameter_objects().items()
                    if value.is_influencer()]))



class TaskDateInfluence(HashInfluenceProvider):
    name = "Date"

    def __init__(self, fmt):
        self.fmt = fmt

    def get_influence(self, task):
        now = datetime.datetime.now()
        return now.strftime(self.fmt)


def _date_influence(fmt):
    def _decorate(cls):
        _old_influence = cls._influence
        def _influence(self, *args, **kwargs):
            influence = _old_influence(self, *args, **kwargs)
            influence.append(TaskDateInfluence(fmt))
            return influence
        cls._influence = _influence
        return cls
    return _decorate


yearly = _date_influence("%Y")
""" Add yearly hash influence.

If nothing else changes, the task is re-executed once every year.

Example:

    .. code-block:: python

        from jolt import influence

        @influence.yearly
        class Example(Task):

"""

weekly = _date_influence("%Y-%w")
""" Add weekly hash influence.

If nothing else changes, the task is re-executed once every week.

Example:

    .. code-block:: python

        from jolt import influence

        @influence.weekly
        class Example(Task):

"""

monthly = _date_influence("%Y-%m")
""" Add monthly hash influence.

If nothing else changes, the task is re-executed once every month.

Example:

    .. code-block:: python

        from jolt import influence

        @influence.monthly
        class Example(Task):

"""

daily = _date_influence("%Y-%m-%d")
""" Add daily hash influence.

If nothing else changes, the task is re-executed once every day.

Example:

    .. code-block:: python

        from jolt import influence

        @influence.daily
        class Example(Task):

"""

hourly = _date_influence("%Y-%m-%d %H")
""" Add hourly hash influence.

If nothing else changes, the task is re-executed once every hour.

Example:

    .. code-block:: python

        from jolt import influence

        @influence.hourly
        class Example(Task):

"""



class TaskEnvironmentInfluence(HashInfluenceProvider):
    name = "Environment"

    def __init__(self, variable):
        self.variable = variable

    def get_influence(self, task):
        return self.variable + "=" + os.environ.get(self.variable, "<unset>")


def environ(variable):
    """ Add environment variable hash influence.

    Args:
        variable (str): Name of an environment variable that will
            influence the hash of the task.

    Example:

    .. code-block:: python

        from jolt import influence

        @influence.environ("CFLAGS")
        class Example(Task):

    """
    def _decorate(cls):
        _old_influence = cls._influence
        def _influence(self, *args, **kwargs):
            influence = _old_influence(self, *args, **kwargs)
            influence.append(TaskEnvironmentInfluence(variable))
            return influence
        cls._influence = _influence
        return cls

    return _decorate


_fi_files = {}


class FileInfluence(HashInfluenceProvider):
    def __init__(self, path):
        self.path = path.rstrip(fs.sep)
        self.name = "File"
        self._files = {}

    def get_file_influence(self, path):
        return utils.filesha1(str(path))

    def get_filelist(self, task):
        try:
            return self._files[task]
        except KeyError:
            if fs.path.isdir(task.tools.expand_path(self.path)):
                path = self.path + fs.sep + "**"
            else:
                path = self.path

            filelist = task.tools.glob(path, expand=True)
            filelist.sort()
            filelist = [Path(fname) for fname in filelist]
            self._files[task] = filelist
            return filelist

    def get_influence(self, task):
        result = []
        for f in self.get_filelist(task):
            if f.is_dir():
                continue
            value = _fi_files.get(f)
            if value:
                result.append(value)
            elif f.exists():
                _fi_files[f] = value = f.name + ":" + self.get_file_influence(f)
                result.append(value)
            elif fs.path.lexists(str(f)):
                _fi_files[f] = value = f.name + ": Symlink (broken)"
                result.append(value)
        return "\n".join(result)

    def is_influenced_by(self, task, path):
        """
        Return True if the path influences the task.
        """
        path = task.tools.expand_path(path)
        return PurePath(path) in self.get_filelist(task)


class DirectoryInfluence(FileInfluence):
    def __init__(self, path):
        super().__init__(path.rstrip(os.sep)+"/**")


def files(pathname):
    """ Add file content hash influence.

    Args:
        pathname (str): A pathname pattern used to find files that will
                influence the hash of the task
                The pattern may contain simple shell-style
                wildcards such as '*' and '?'. Note: files starting with a
                dot are not matched by these wildcards.

    Example:

    .. code-block:: python

        from jolt import influence

        @influence.files("*.cpp")
        class Example(Task):

    """
    def _decorate(cls):
        _old_influence = cls._influence
        def _influence(self, *args, **kwargs):
            influence = _old_influence(self, *args, **kwargs)
            influence.append(FileInfluence(pathname))
            return influence
        cls._influence = _influence
        return cls

    return _decorate


def global_files(pathname, cls=FileInfluence):
    HashInfluenceRegistry.get().register(cls(pathname))


class WhitelistInfluence(FileInfluence):
    def __init__(self, path):
        self.path = path.rstrip(fs.sep)
        self.name = "Whitelist"

    def get_influence(self, task):
        return self.path

    def is_influenced_by(self, task, path):
        path = task.tools.expand_path(path)
        pattern = task.tools.expand_path(self.path)
        return utils.pathmatch(path, pattern)


def whitelist(pathname):
    """
    Whitelist files published by a task, but don't let them influence
    the hash.

    This is typically used to whitelist files in the workspace. It
    should only be used for files produced by the task, not for files
    used as input. If possible, consider writing files to build
    directories instead.

    This decorator cannot be used to exclude influencing files matched
    by another influence decorator. If there is an overlap of files
    between decorators, some or all of the overlapping files files may
    influence the hash.

    Args:
        pathname (str): A pathname pattern used to match whitelisted files.
                The pattern may contain simple shell-style
                wildcards such as '*' and '?'. Note: files starting with a
                dot are not matched by these wildcards.

    Example:

    .. code-block:: python

        from jolt import influence

        @influence.whitelist("build/")
        class Example(Task):

    """
    def _decorate(cls):
        _old_influence = cls._influence
        def _influence(self, *args, **kwargs):
            influence = _old_influence(self, *args, **kwargs)
            influence.append(WhitelistInfluence(pathname))
            return influence
        cls._influence = _influence
        return cls

    return _decorate


class StringInfluence(HashInfluenceProvider):
    name = "String"

    def __init__(self, value):
        self.value = value

    def get_influence(self, task):
        return self.value


def global_string(string):
    HashInfluenceRegistry.get().register(StringInfluence(string))
