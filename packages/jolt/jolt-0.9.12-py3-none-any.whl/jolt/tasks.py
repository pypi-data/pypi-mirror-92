import base64
import copy
import fnmatch
import functools
import inspect
from pathlib import Path
import platform
import subprocess
import sys
import unittest as ut

from jolt import filesystem as fs
from jolt import log
from jolt import utils
from jolt.cache import ArtifactAttributeSetProvider
from jolt.error import raise_task_error, raise_task_error_if
from jolt.expires import Immediately
from jolt.influence import FileInfluence, TaskSourceInfluence, TaintInfluenceProvider
from jolt.influence import source as source_influence, attribute as attribute_influence
from jolt.tools import Tools


class Export(object):
    def __init__(self, value, encoded=False):
        self._imported = False
        self._task = None
        self._value = None
        self.exported_value = value
        self.encoded = encoded

    @property
    def value(self):
        if self._value is None:
            self._value = self.exported_value(self._task)
        return self._value

    @property
    def is_imported(self):
        return self._imported

    def assign(self, value):
        value = value or ""
        self._value = base64.decodebytes(value.encode()).decode() if self.encoded else value
        self._imported = True

    def export(self, task):
        value = self.value
        if value:
            value = base64.encodebytes(value.encode()).decode() if self.encoded else value
        return value

    def set_task(self, task):
        self._task = task



class Parameter(object):
    """ Generic task parameter type. """

    def __init__(self, default=None, values=None, required=True,
                 const=False, influence=True, help=None):
        """
        Creates a new parameter.

        Args:
            default (str, optional): An optional default value.
            values (list, optional): A list of accepted values. An
                assertion is raised if an unlisted value is assigned to the parameter.
            required (boolean, optional): If required, the parameter must be assigned
                a value before the task can be executed. The default is ``True``.
            const (boolean, optional): If const is True, the parameter is immutable
                and cannot be assigned a non-default value. This is useful in
                a class hierarchy where a subclass may want to impose restrictions
                on a parent class parameter. The default is ``False``.
            influence (boolean, optional): If influence is False, the parameter value
                will not influence the identity of the task artifact. The default is
                True.
            help (str, optional): Documentation for the parameter.
                This text is displayed when running the ``info`` command on the
                associated task.

        Raises:
            ValueError: If the parameter is assigned an illegal value.

        """

        self._default = default
        self._value = default
        self._accepted_values = values
        self._required = required
        self._const = const
        self._influence = influence
        self.__doc__ = help
        if default:
            self._validate(default)

    def __str__(self):
        """ Returns the parameter value as a string """
        return str(self._value) if self._value is not None else ''

    def _validate(self, value):
        if self._accepted_values is not None and value not in self._accepted_values:
            raise ValueError(value)

    def get_default(self):
        """ Get the default value of the parameter.

        Returns:
            The default value or None if no default was given.
        """
        return self._default

    @property
    def default(self):
        """ Get the default value of the parameter.

        Returns:
            The default value or None if no default was given.
        """
        return self._default

    def set_default(self, value):
        """ Set the default value of the parameter.

        Args:
            value (str): The new default value of the parameter.
        """
        self._validate(value)
        if self.is_default():
            self._value = value
        self._default = value

    def is_influencer(self):
        """ Check if the parameter value influences the identitiy of the task artifact.

        Returns:
            True if the parameter influences the identity, False otherwise.
        """
        return self._influence

    def is_required(self):
        """ Check if the parameter must be set to a value.

        Returns:
            True if the parameter must be assigned a value, False otherwise.
        """
        return self._required

    def is_default(self):
        """ Check if parameter is set to its default value.

        Returns:
            True if the assigned value is the default value.
        """
        return self._default == self._value

    def is_unset(self):
        """ Check if the parameter is unset.

        Returns:
            True if the assigned value is None.
        """
        return self._value is None

    def is_set(self):
        """ Check if the parameter is set to a non-default value.

        Returns:
            True if the assigned value is not the default value.
        """
        return not self.is_unset() and not self.is_default()

    def is_const(self):
        """ Check if the parameter can be assigned or not.

        Returns:
            True if the parameter is immutable.
        """
        return self._const

    def get_value(self):
        """ Get the parameter value. """
        return self._value

    @property
    def value(self):
        """ Get the parameter value. """
        return self._value

    def __bool__(self):
        """ Returns True if the parameter value is a non-empty string. """
        return self._value is not None and self._value != ""

    def __eq__(self, value):
        """ Compare parameter value """
        return self._value == value

    def set_value(self, value):
        """ Set the parameter value.

        Args:
            value (str): The new parameter value.

        Raises:
            ValueError: If the parameter is assigned an illegal value.
        """
        self._validate(value)
        if self._const and value != self._default:
            raise ValueError("immutable")
        self._value = value


class BooleanParameter(Parameter):
    """ Boolean task parameter type. """

    def __init__(self, default=None, required=True, const=False, influence=True, help=None):
        """
        Creates a new parameter.

        Args:
            default (boolean, optional): An optional default boolean value.
            required (boolean, optional): If required, the parameter must be assigned
                a value before the task can be executed. The default is ``True``.
            const (boolean, optional): If const is True, the parameter is immutable
                and cannot be assigned a non-default value. This is useful in
                a class hierarchy where a subclass may want to impose restrictions
                on a parent class parameter. The default is ``False``.
            influence (boolean, optional): If influence is False, the parameter value
                will not influence the identity of the task artifact. The default is
                True.
            help (str, optional): Documentation for the parameter.
                This text is displayed when running the ``info`` command on the
                associated task.

        Raises:
            ValueError: If the parameter is assigned an illegal value.

        """
        default = str(default).lower() if default is not None else None
        super(BooleanParameter, self).__init__(
            default,
            values=["false", "true", "0", "1", "no", "yes"],
            required=required,
            const=const,
            influence=influence,
            help=help)

    def set_value(self, value):
        """ Set the parameter value.

        Args:
            value (boolean): The new parameter value. Accepted values are:
                False, True, "false, and "true", 0 and 1, "no" and "yes".

        Raises:
            ValueError: If the parameter is assigned an illegal value.
        """
        value = str(value).lower()
        super(BooleanParameter, self).set_value(value)

    @property
    def is_true(self):
        """ The parameter value is True. """
        return str(self.get_value()) in ["true", "1", "yes"]

    @property
    def is_false(self):
        """ The parameter value is False. """
        return not self.is_true

    def __bool__(self):
        return self.is_true

    def __getitem__(self, key):
        """
        Returns a substitution string depending on the parameter value.

        Args:
            key (str): A special key syntax, ``enabled,disabled``, where
            and either ``enabled`` or ``disabled`` would be returned
            depending on the paramter value. See the example below.

        Returns:
            Substitution string.

        Example:

          .. code-block:: python

            class Example(Task):
               debug = BooleanParameter()

               def run(self, deps, tools):
                   self.info("debug is {debug[enabled,disabled]}")

          .. code-block:: bash

            $ jolt build example:debug=true
            [INFO] debug is enabled (example)

            $ jolt build example:debug=false
            [INFO] debug is disabled (example)

        """
        key = key.split(",")
        if len(key) != 2:
            raise KeyError(key)
        return key[0] if self.is_true else key[1]



class ListParameter(Parameter):
    """ List parameter type.

    A list parameter allows multiple values to be assigned to it. Values are
    separated by the '+' character in qualified task names. Each assigned value
    is validated against the list of accepted values. They are sorted in
    alphabetical order before the task is executed.

    Example:

      .. code-block:: python

        class Example(Task):
            arg = ListParameter(default=["c"], values=["a", "b", "c"], help="A list parameter")

            def run(self, deps, tools):
                for item in self.arg:
                    print(item)

      .. code-block:: bash

        $ jolt build example example:arg=a example:arg=a+b

    """

    def __init__(self, *args, **kwargs):
        """
        Creates a new list parameter.

        Args:
            default (boolean, optional): An optional list of default values.
            values (list, optional): A list of accepted values. An
                assertion is raised if an unlisted value is assigned to the parameter.
            required (boolean, optional): If required, the parameter must be assigned
                a value before the task can be executed. The default is ``True``.
            const (boolean, optional): If const is True, the parameter is immutable
                and cannot be assigned a non-default value. This is useful in
                a class hierarchy where a subclass may want to impose restrictions
                on a parent class parameter. The default is ``False``.
            influence (boolean, optional): If influence is False, the parameter value
                will not influence the identity of the task artifact. The default is
                True.
            help (str, optional): Documentation for the parameter.
                This text is displayed when running the ``info`` command on the
                associated task.

        Raises:
            ValueError: If the parameter is assigned an illegal value.

        """
        super().__init__(*args, **kwargs)

    def set_value(self, value):
        """ Set the parameter value.

        Args:
            value (boolean): The new parameter value. Accepted values are:
                False, True, "false, and "true", 0 and 1, "no" and "yes".

        Raises:
            ValueError: If the parameter is assigned an illegal value.
        """
        value = str(value).split("+") if type(value) == str else value
        value.sort()
        super().set_value(value)

    def _validate(self, value):
        if self._accepted_values is not None:
            for item in value:
                if item not in self._accepted_values:
                    raise ValueError(item)

    def get_value(self):
        return "+".join(self._value)

    def __bool__(self):
        """ Returns True if the list is non-empty. """
        return len(self._value) > 0

    def __iter__(self):
        """ Returns a sequence iterator. """
        return iter(self._value)

    def __len__(self):
        """ Returns the length of the list. """
        return len(self._value)

    def __getitem__(self, key):
        """
        Returns an element or a slice from the list.

        Args:
            key (int, slice, str): Element index or slice. A key string can
            be used to check for the existence of that value in the list.
            If the key is present the same value is returned, otherwise None.

            A special key syntax is also available to request an alternate return
            value depending on the presence of the key. Instead of a list value
            you pass ``value,present,absent`` and either ``present`` or ``absent``
            will be returned. See the example below.

        Returns:
            Element value, or substitution.

        Example:

          .. code-block:: python

            class Example(Task):
               features = ListParameter(values=["optimize", "strip"], required=False)

               def run(self, deps, tools):
                   if len(self.features) > 0:
                       self.info("first feature is {features[0]}")
                       self.info("optimize == {features[optimize]}")
                       self.info("optimization is {features[optimize,enabled,disabled]}")

          .. code-block:: bash

            $ jolt build example:features=optimize+strip
            [INFO] first feature is optimize (example)
            [INFO] optimize = optimize (example)
            [INFO] optimization is enabled (example)

            $ jolt build example:features=strip
            [INFO] first feature is debug (example)
            [INFO] optimize = None (example)
            [INFO] optimization is disabled (example)

        """
        if type(key) == str:
            key = key.split(",")
            if len(key) == 1:
                true = key[0]
                false = None
            else:
                true = key[1] if len(key) > 1 else key[0]
                false = key[2] if len(key) > 2 else None
            return true if key[0] in self._value else false
        return self._value[key]


class TaskRegistry(object):
    _instance = None

    def __init__(self, env=None):
        self.env = env
        self.tasks = {}
        self.tests = {}
        self.instances = {}

    @staticmethod
    def get(*args, **kwargs):
        if not TaskRegistry._instance:
            TaskRegistry._instance = TaskRegistry(*args, **kwargs)
        return TaskRegistry._instance

    def add_task_class(self, cls):
        self.tasks[cls.name] = cls

    def add_test_class(self, cls):
        self.tests[cls.name] = cls

    def add_task(self, task, extra_params):
        name, params = utils.parse_task_name(task.name)
        params.update(extra_params or {})
        full_name = utils.format_task_name(name, params)
        self.instances[full_name] = task

    def get_task_class(self, name):
        return self.tasks.get(name)

    def get_test_class(self, name):
        return self.tests.get(name)

    def get_task_classes(self):
        return list(self.tasks.values())

    def get_test_classes(self):
        return list(self.tests.values())

    def _apply_task_manifest(self, task, manifest=None):
        if manifest is None:
            return
        manifest_task = manifest.find_task(task.qualified_name)
        if manifest_task is not None:
            if manifest_task.identity:
                task.identity = manifest_task.identity
            for attrib in manifest_task.attributes:
                export = utils.getattr_safe(task, attrib.name)
                assert isinstance(export, Export), \
                    "'{0}' is not an exportable attribute of task '{1}'"\
                    .format(attrib.name, task.qualified_name)
                export.assign(attrib.value)

    def get_task(self, name, extra_params=None, manifest=None):
        name, params = utils.parse_task_name(name)
        params.update(extra_params or {})
        full_name = utils.format_task_name(name, params)

        task = self.instances.get(full_name)
        if task:
            return task

        cls = self.tasks.get(name)
        if cls:
            task = cls(parameters=params)
            task = self.instances.get(task.qualified_name, task)
            self._apply_task_manifest(task, manifest)
            self.instances[task.qualified_name] = task
            self.instances[full_name] = task
            return task

        cls = self.tests.get(name)
        if cls:
            task = _Test(cls, parameters=params)
            task = self.instances.get(task.qualified_name, task)
            self._apply_task_manifest(task, manifest)
            self.instances[task.qualified_name] = task
            self.instances[full_name] = task
            return task

        raise_task_error_if(not task, full_name, "no such task")

    def set_default_parameters(self, task):
        name, params = utils.parse_task_name(task)

        cls = self.tasks.get(name)
        if not cls:
            cls = self.tests.get(name)
        raise_task_error_if(not cls, task, "no such task")
        cls._set_default_parameters(cls, params)

    def set_joltdir(self, joltdir):
        for task in list(self.tasks.values()) + list(self.tests.values()):
            task.joltdir = joltdir

    def _create_parents(self, name):
        names = name.split("/")

        if len(names) <= 1:
            return

        prev = None
        for i in reversed(range(0, len(names))):
            name = "/".join(names[:i + 1])
            task = self.instances.get(name) or Task(name)
            if prev:
                task.requires += [prev.name]
            prev = task


class TaskGenerator(object):
    """
    Base class for task generators.

    Generators create tasks classes dynamically in runtime.
    They are used to implement concepts such as components
    where multiple similar tasks should be created.

    For example, a C++ library should not only be built, it
    should also be tested. While it is possible to add one
    task for the compilation of the library and another for
    the test, it is advisable to instead use a task generator
    when there are multiple libraries to build and test.
    The generator will ensure that all libraries are built and
    tested identically. Additional tasks, such as sourcedoc
    generation, can be added for all libraries at a later
    point in time. Refactoring is simplified by gathering
    shared code in one place.

    Generated tasks can be replaced by defining a task with
    the same name explicitly.

    """

    abstract = True
    """ An abstract task generator class indended to be subclassed.

    Abstract task generators are not invoked.
    """

    def generate(self):
        """
        Generate tasks.

        Called by Jolt during the parsing of user task
        definitions.

        Returns:
            A list of task classes to be registered with Jolt.

        """
        raise NotImplementedError()



class attributes:
    @staticmethod
    def requires(attrib):
        """
        Decorates a task with an alternative ``requires`` attribute.

        The new attribute will be concatenated with the regular
        ``requires`` attribute.

        Args:
            attrib (str): Name of alternative attribute.
                Keywords are expanded.
        """
        return utils.concat_attributes("requires", attrib)

    @staticmethod
    def attribute(alias, target, influence=True):
        """
        Decorates a task with an alias for another attribute.

        Args:
            attrib (str): Name of alias attribute.
            target (str): Name of target attribute.
                Keywords are expanded.
            influence (boolean): Add value of target
                attribute as influence of the task.

        """
        def _decorate(cls):
            def _get(self):
                return getattr(self, self.expand(target))
            setattr(cls, alias, property(_get))
            if influence:
                attribute_influence(target)(cls)
            return cls
        return _decorate


    @staticmethod
    def method(alias, target, influence=True):
        """
        Decorates a task with an alias for another method.

        Args:
            attrib (str): Name of alias method.
            target (str): Name of target method.
                Keywords are expanded.
            influence (boolean): Add source of target
                method as influence of the task.

        """
        def _decorate(cls):
            def _call(self, *args, **kwargs):
                return getattr(self, self.expand(target))(*args, **kwargs)
            setattr(cls, alias, _call)
            if influence:
                source_influence(target)(cls)
            return cls
        return _decorate


    @staticmethod
    def system(cls):
        """
        Decorates a task with a property returning the operating system name.

        Examples: "linux", "windows"
        """
        cls.system = property(lambda t: platform.system().lower())
        return cls


class TaskBase(object):
    """ Task base class """

    cacheable = True
    """ Whether the task produces an artifact or not. """

    expires = Immediately()
    """An expiration strategy, defining when the artifact may be evicted from the cache.

    When the size of the artifact cache exceeds the configured limit
    an attempt will be made to evict artifacts from the cache. The eviction
    algorithm processes artifacts in least recently used (LRU) order until
    an expired artifact is found.

    By default, an artifact expires immediately and may be evicted at any time
    (in LRU order). An exception to this rule is if the artifact is required by
    a task in the active task set. For example, if a task A requires the output
    of task B, B will never be evicted by A while A is being executed.

    There are several expiration strategies to choose from:

     - :class:`jolt.expires.WhenUnusedFor`
     - :class:`jolt.expires.After`
     - :class:`jolt.expires.Never`

    Examples:

        .. code-block:: python

          # May be evicted if it hasn't been used for 15 days
          expires = WhenUnusedFor(days=15)

        .. code-block:: python

          # May be evicted 1h after creation
          expires = After(hours=1)

        .. code-block:: python

          # Never evicted
          expires = Never()

    """

    extends = ""
    """
    Name of extended task.

    A task with this attribute set is called an extension. An extension
    is executed in the context of the extended task, immediately after
    the extended task has executed.

    A common use-case for extensions is to produce additional artifacts
    from the output of another task. Also, for long-running tasks, it is
    sometimes beneficial to utilize the intermediate output from an extended
    task. The extension artifact can then be acquired more cheaply than if the
    extension had performed all of the work from scratch.

    An extension can only extend one other task.
    """

    fast = False
    """
    Indication of task speed.

    The information is used by the distributed execution strategy to
    optimize how tasks are scheduled. Scheduling tasks remotely is always
    associated with some overhead and sometimes it's beneficial to instead
    schedule fast tasks locally if possible.

    An extended task is only considered fast if all extensions are fast.
    """

    influence = []
    """ List of influence provider objects """

    joltdir = "."
    """ Path to the directory of the .jolt file where the task was defined. """

    joltproject = None
    """ Name of project this task belongs to. """

    name = None
    """ Name of the task. Derived from class name if not set. """

    requires = []
    """ List of dependencies to other tasks. """

    selfsustained = False
    """ Consume this task independently of its requirements.

    Requirements of a self-sustained task will be pruned if the task artifact
    is present in a cache. In other words, if the task is not executed its
    requirements are considered unnecessary.

    For example, consider the task graph A -> B -> C. If B is self-sustained
    and present in a cache, C will never be executed. C will also never be a
    transitive requirement of A. If A requires C, it should be listed
    as an explicit requirement.

    Using this attribute speeds up execution and reduces network
    traffic by allowing the task graph to be reduced.
    """

    taint = None
    """ An arbitrary value used to change the identity of the task.

    It may be hard to remove bad artifacts in a distributed build
    environment. A better method is to taint the task and let the
    artifact be recreated with a different identity.
    """

    weight = 0
    """
    Indication of task execution time.

    The weight is used to optimize the order in which tasks are
    executed using a heuristic scheduling algorithm where ready
    tasks along the critical path are favored.
    """

    def __init__(self, parameters=None, **kwargs):
        self._identity = None
        self.name = self.__class__.name

        self._create_exports_and_parameters()
        self._set_parameters(parameters)

        self.cacheable = self.__class__.cacheable
        self.extends = self.expand(utils.call_or_return_list(self, self.__class__.extends))
        raise_task_error_if(
            len(self.extends) != 1, self,
            "multiple tasks extended, only one allowed")
        self.extends = self.extends[0]
        self.influence = utils.call_or_return_list(self, self.__class__._influence)
        self.influence.append(TaskSourceInfluence("publish"))
        self.influence.append(TaskSourceInfluence("run"))
        self.influence.append(TaskSourceInfluence("unpack"))
        self.influence.append(TaintInfluenceProvider())
        self.requires = self.expand(utils.unique_list(utils.call_or_return_list(self, self.__class__._requires)))
        self.selfsustained = utils.call_or_return(self, self.__class__._selfsustained)
        self.tools = Tools(self, self.joltdir)

    def _influence(self):
        return utils.as_list(self.__class__.influence)

    def _requires(self):
        return utils.call_or_return_list(self, self.__class__.requires)

    def _selfsustained(self):
        return utils.call_or_return(self, self.__class__.selfsustained)

    def _get_source(self, func):
        source, _ = inspect.getsourcelines(func)
        return "\n".join(source)

    def _create_exports_and_parameters(self):
        self._exports = {}
        self._parameters = {}
        for key in dir(self):
            obj = utils.getattr_safe(self, key)
            if isinstance(obj, Export):
                export = copy.copy(obj)
                setattr(self, key, export)
                self._exports[key] = export
                export.set_task(self)
            if isinstance(obj, Parameter):
                param = copy.copy(obj)
                setattr(self, key, param)
                self._parameters[key] = param

    def _set_parameters(self, params):
        params = params or {}
        for key, value in params.items():
            try:
                param = utils.getattr_safe(self, key)
            except AttributeError as e:
                raise_task_error(self, "no such parameter '{0}'", key)
            if isinstance(param, Parameter):
                try:
                    param.set_value(value)
                except ValueError as e:
                    raise_task_error(
                        self,
                        "illegal value '{0}' assigned to parameter '{1}'",
                        str(e), key)
                continue
            raise_task_error(self, "no such parameter '{0}'", key)
        self._assert_required_parameters_assigned()

    @staticmethod
    def _set_default_parameters(cls, params):
        params = params or {}
        for key, value in params.items():
            param = utils.getattr_safe(cls, key)
            if isinstance(param, Parameter):
                param = copy.copy(param)
                param.set_default(value)
                setattr(cls, key, param)
                continue
            raise_task_error(cls.name, "no such parameter '{0}'", key)

    def _assert_required_parameters_assigned(self):
        for key, param in self._get_parameter_objects().items():
            raise_task_error_if(
                param.is_required() and param.is_unset(), self,
                "required parameter '{0}' has not been set", key)

    def _verify_influence(self, deps, artifact, tools, sources=None):
        # Verify that any transformed sources are influencing
        sources = set(map(tools.expand_path, sources or []))

        # Verify that published files are influencing
        for src, _ in artifact.files.items():
            src = tools.expand_path(src)
            if fs.path.isdir(src):
                sources.update(fs.scandir(src))
            else:
                sources.add(src)

        def _subpath_filter(rootpath):
            def _filter(fname):
                return not fs.is_relative_to(fname, rootpath)
            return _filter

        for _, dep in deps.items():
            deptask = dep.get_task()
            if isinstance(deptask, FileInfluence):
                # Resource dependencies may cover the influence implicitly
                deppath = self.tools.expand_path(str(deptask.path))
                sources = set(filter(lambda d: not deptask.is_influenced_by(self, d), sources))
            else:
                # Ignore any files in artifacts
                deppath = self.tools.expand_path(dep.path)
                sources = set(filter(_subpath_filter(deppath), sources))

        # Ignore any files in build directories
        sources = filter(_subpath_filter(tools.expand_path(tools.buildroot)), sources)
        sources = set(sources)

        for ip in self.influence:
            if not isinstance(ip, FileInfluence):
                continue
            ok = [source for source in sources if ip.is_influenced_by(self, source)]
            sources.difference_update(ok)
        for source in sources:
            log.warning("Missing influence: {} ({})", source, self.name)
        raise_task_error_if(sources, self, "task is missing source influence")

    @utils.cached.instance
    def _get_export_objects(self):
        return self._exports

    @utils.cached.instance
    def _get_parameter_objects(self, unset=False):
        return self._parameters

    def _get_parameters(self, unset=False):
        return {
            key: param.get_value()
            for key, param in self._get_parameter_objects().items()
            if unset or not param.is_unset()
        }

    def _get_explicitly_set_parameters(self):
        return {
            key: param.get_value()
            for key, param in self._get_parameter_objects().items()
            if param.is_set()
        }

    def __str__(self):
        return str(self.name)

    @property
    def canonical_name(self):
        return utils.canonical(self.name)

    @property
    def qualified_name(self):
        return utils.format_task_name(
            self.name,
            self._get_parameters())

    @property
    def short_qualified_name(self):
        return utils.format_task_name(
            self.name,
            self._get_explicitly_set_parameters())

    def expand(self, string_or_list, *args, **kwargs):
        """ Expands keyword arguments/macros in a format string.

        See :func:`jolt.Tools.expand` for details.
        """

        try:
            kwargs["_instance"] = self
            if type(string_or_list) == list:
                return [utils.expand(string, *args, **kwargs) for string in string_or_list]
            return utils.expand(string_or_list, *args, **kwargs)
        except KeyError as e:
            raise_task_error(self, "invalid macro '{0}' encountered - forgot to set a parameter?", e)

    @property
    def identity(self):
        return self._identity

    @identity.setter
    def identity(self, identity):
        self._identity = identity

    def is_cacheable(self):
        return self.cacheable

    def is_runnable(self):
        return True


class Task(TaskBase):
    #: Path to the .jolt file where the task was defined.

    abstract = True
    """ An abstract task class indended to be subclassed.

    Abstract tasks can't be executed and won't be listed.
    """

    def __init__(self, parameters=None, **kwargs):
        super(Task, self).__init__(parameters, **kwargs)

    def info(self, fmt, *args, **kwargs):
        """
        Log information about the task.
        """
        fmt = self.tools.expand(fmt, *args, **kwargs)
        log.info(fmt, *args, **kwargs)

    def warning(self, fmt, *args, **kwargs):
        """ Log a warning concerning the task """
        fmt = self.tools.expand(fmt, *args, **kwargs)
        log.warning(fmt, *args, **kwargs)

    def error(self, fmt, *args, **kwargs):
        """ Log an error concerning the task """
        fmt = self.tools.expand(fmt, *args, **kwargs)
        log.error(fmt, *args, **kwargs)

    def clean(self, tools):
        """
        Cleans up resources and intermediate files created by the task.

        The method is invoked in response to the user running clean
        on the command line. It should restore the environment to its
        original state. The next execution of the task should behave
        as if the task is executed for the first time.

        An implementation must not clean any local or remote artifact cache.
        """
        pass

    def run(self, deps, tools):
        """
        Performs the work of the task.

        Dependencies specified with "requires" are passed as the
        deps dictionary. The tools argument provides a set of low
        level tool functions that may be useful.

        .. code-block:: python

          with tools.cwd("path/to/subdir"):
              tools.run("make {target}")

        When using methods from the toolbox, task parameters, such
        as ``target`` above,  are automatically expanded to their values.
        """
        pass

    def publish(self, artifact, tools):
        """
        Publishes files produced by :func:`~run`.

        Files can be collected in to the artifact by calling
        artifact.collect().

        Additional metadata can be provided, such as environment
        variables that should be set whenever the task artifact is
        consumed. Example:

        .. code-block:: python

          # Append <artifact-path>/bin to the PATH
          artifact.environ.PATH.append("bin")

          # Pass an arbitrary string to a consumer
          artifact.strings.foo = "bar"

        """
        pass

    def unpack(self, artifact, tools):
        """
        Unpacks files published by publish() .

        The intention of this hook is to make necessary adjustments
        to artifact files and directories once they have been downloaded
        into the local cache on a different machine. For example,
        paths may have to be adjusted or an installer executed.

        This hook is executed in the context of a consuming task.
        """
        raise NotImplementedError()

    def shell(self, deps, tools):
        """
        Invoked to start a debug shell.

        The method prepares the environment with attributes exported by task requirement
        artifacts. The shell is entered by passing the ``-g`` flag to the build command.

        Task execution resumes normally when exiting the shell.
        """
        with tools.environ(PS1="jolt$ ") as env:
            from jolt import config
            subprocess.call(config.get_shell().split(), env=env, cwd=tools._cwd)


class Resource(Task):
    """
    A resource task.

    Resources are special tasks executed in the :class:`~jolt.Context` of other tasks.
    They are invoked to acquire and release a resource, such as hardware equipment,
    before and after the execution of a task. No artifact is produced by a resource.

    Implementors should override :func:`~acquire` and :func:`~release`.

    """

    cacheable = False

    abstract = True
    """ An abstract resource class indended to be subclassed. """

    def __init__(self, *args, **kwargs):
        super(Resource, self).__init__(*args, **kwargs)
        self.influence.append(TaskSourceInfluence("acquire"))
        self.influence.append(TaskSourceInfluence("release"))

    def is_runnable(self):
        return False

    def info(self, fmt, *args, **kwargs):
        pass

    def acquire(self, artifact, deps, tools):
        """ Called to acquire the resource.

        An implementor overrides this method in a subclass. The acquired
        resource must be released manually if an exception occurs before the
        method has returned.

        Args:
            artifact (:class:`~jolt.Artifact`): The artifact associated with the resource.
                It is not possible to publish files from a resource, but the implementor
                can still use the resource to pass information to consuming tasks.
            deps (:class:`~jolt.Context`): Task execution context used to access the
                artifacts of dependencies.
            tools (:class:`~jolt.Tools`): A task specific toolbox.

        """
        pass

    def release(self, artifact, deps, tools):
        """ Called to release the resource.

        An implementor overrides this method in a subclass.

        Args:
            artifact (:class:`~jolt.Artifact`): The artifact associated with the resource.
                It is not possible to publish files from a resource, but the implementor
                can still use the resource to pass information to consuming tasks.
            deps (:class:`~jolt.Context`): Task execution context used to access the
                artifacts of dependencies.
            tools (:class:`~jolt.Tools`): A task specific toolbox.
        """
        pass

    def run(self, env, tools):
        self._run_env = env


class WorkspaceResource(Resource):
    """
    A workspace resource task.

    A workspace resource is a similiar to a regular resource and may be used as such,
    but it can also be used from a workspace manifest to acquire project resources
    before any task recipes are parsed. A common use-case is to retrieve project
    sources from SCM. Workspace resources cannot have any dependencies.
    No artifact is produced.

    Implementors should override :func:`~acquire_ws` and :func:`~release_ws`.
    """

    def __init__(self, *args, **kwargs):
        super(WorkspaceResource, self).__init__(*args, **kwargs)
        raise_task_error_if(len(self.requires) > 0, self,
                            "workspace resource is not allowed to have requirements")

    def acquire(self, artifact, deps, tools):
        return self.acquire_ws()

    def release(self, artifact, deps, tools):
        return self.release_ws()

    def acquire_ws(self):
        """ Called to acquire the resource.

        An implementor overrides this method in a subclass. The acquired
        resource must be released manually if an exception occurs before the
        method has returned. """
        pass

    def release_ws(self):
        """ Called to release the resource.

        An implementor overrides this method in a subclass.

        """
        pass


class Alias(Task):
    """
    An alias task.

    Aliases are a special kind of task which can be used to introduce new
    names for other tasks or groups of tasks. They are useful as milestones
    when building continuous integration pipelines since they won't
    be executed, thus saving time compared to a regular task.
    """

    cacheable = False

    abstract = True
    """ An abstract alias class indended to be subclassed. """

    def __init__(self, *args, **kwargs):
        super(Alias, self).__init__(*args, **kwargs)
        raise_task_error_if(
            self.extends, self, "aliases cannot be extensions")

    def is_runnable(self):
        return False

    def info(self, fmt, *args, **kwargs):
        pass


class TaskException(Exception):
    def __init__(self, *args, **kwargs):
        super(TaskException, self).__init__(*args, **kwargs)



__unittest = True


class _TestCase(ut.FunctionTestCase):
    def __init__(self, task, deps, tools, testfunc, *args, **kwargs):
        super().__init__(testfunc, *args, **kwargs)
        self.task = task
        self.deps = deps
        self.tools = tools
        self.testfunc = testfunc

    @property
    def name(self):
        return self.testfunc.__name__

    @property
    def fullname(self):
        return "{}.{}".format(self.task.__class__.__name__, self.name)

    def runTest(self):
        self.task._run(self)

    def __str__(self):
        return "{} ({})".format(self.task.__class__.__name__, self.testfunc.__name__)

    @property
    def __doc__(self):
        return self.testfunc.__doc__


class _TestResult(ut.TextTestResult):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.successes = []

    def _begin(self):
        log.stdout(ut.TextTestResult.separator1)

    def _end(self):
        log.stdout(ut.TextTestResult.separator2)
        log.stdout("")

    def startTest(self, test):
        self._begin()
        super().startTest(test)
        log.stdout(ut.TextTestResult.separator2)

    def addSuccess(self, test):
        super().addSuccess(test)
        self.successes.append(test)
        self._end()

    def addError(self, test, err):
        super().addError(test, err)
        self._end()

    def addFailure(self, test, err):
        super().addFailure(test, err)
        self._end()

    def addSkip(self, test, reason):
        super().addSkip(test, reason)
        self._end()



class Test(Task):
    """ A test task.

    The test task combines a regular Jolt task with a Python ``unittest.TestCase``.
    As such, a test task is a collection of similar test-cases where each test-case
    is implemented as an instancemethod named with a ``test_`` prefix. When executed,
    the task runs all test-case methods and summarizes the result.

    All regular ``unittest`` assertions and decorators can be used in the test methods.
    For details about inherited task attributes, see :class:`jolt.tasks.Task` and
    Python unittest.TestCase.

    Example:

    .. code-block:: python

      class OperatorTest(Test):

          def test_add(self):
              self.assertEqual(1+1, 2)

          def test_sub(self):
              self.assertEqual(2-1, 1)

    """

    abstract = True
    """ An abstract test class indended to be subclassed.

    Abstract test tasks can't be executed and won't be listed.
    """

    pattern = Parameter(required=False, help="Test-case filter wildcard.")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.influence.append(TaskSourceInfluence("setup", self))
        self.influence.append(TaskSourceInfluence("cleanup", self))
        for name in self._get_test_names():
            self.influence.append(TaskSourceInfluence(name, self))

    def setup(self, deps, tools):
        """ Implement this method to make preparations before a test """

    def cleanup(self):
        """ Implement this method to clean up after a test """

    def skip(self, reason=""):
        raise ut.SkipTest(self.tools.expand(reason))

    def _get_test_names(self):
        return [attrib for attrib in dir(self) if attrib.startswith("test_")]

    def _setup(self, test):
        self._curtest = test
        self._testMethodName = test.testfunc.__name__
        self._testMethodDoc = test.testfunc.__doc__
        self.setup(test.deps, test.tools)

    def _test(self, test):
        test.testfunc()

    def _cleanup(self, test):
        self.cleanup()

    def _run(self, test):
        try:
            self._setup(test)
            self._test(test)
        finally:
            self._cleanup(test)

    def assertTrue(self, *args, **kwargs):
        return self._curtest.assertTrue(*args, **kwargs)

    def assertFalse(self, *args, **kwargs):
        return self._curtest.assertFalse(*args, **kwargs)

    def assertIn(self, *args, **kwargs):
        return self._curtest.assertIn(*args, **kwargs)

    def assertNotIn(self, *args, **kwargs):
        return self._curtest.assertNotIn(*args, **kwargs)

    def assertIs(self, *args, **kwargs):
        return self._curtest.assertIs(*args, **kwargs)

    def assertIsNot(self, *args, **kwargs):
        return self._curtest.assertIsNot(*args, **kwargs)

    def assertIsInstance(self, *args, **kwargs):
        return self._curtest.assertIsInstance(*args, **kwargs)

    def assertIsNotInstance(self, *args, **kwargs):
        return self._curtest.assertIsNotInstance(*args, **kwargs)

    def assertIsNone(self, *args, **kwargs):
        return self._curtest.assertIsNone(*args, **kwargs)

    def assertIsNotNone(self, *args, **kwargs):
        return self._curtest.assertIsNotNone(*args, **kwargs)

    def assertEqual(self, *args, **kwargs):
        return self._curtest.assertEqual(*args, **kwargs)

    def assertNotEqual(self, *args, **kwargs):
        return self._curtest.assertNotEqual(*args, **kwargs)

    def assertAlmostEqual(self, *args, **kwargs):
        return self._curtest.assertAlmostEqual(*args, **kwargs)

    def assertAlmostNotEqual(self, *args, **kwargs):
        return self._curtest.assertAlmostNotEqual(*args, **kwargs)

    def assertGreater(self, *args, **kwargs):
        return self._curtest.assertGreater(*args, **kwargs)

    def assertGreaterEqual(self, *args, **kwargs):
        return self._curtest.assertGreaterEqual(*args, **kwargs)

    def assertLess(self, *args, **kwargs):
        return self._curtest.assertLess(*args, **kwargs)

    def assertLessEqual(self, *args, **kwargs):
        return self._curtest.assertLessEqual(*args, **kwargs)

    def assertRaises(self, *args, **kwargs):
        return self._curtest.assertRaises(*args, **kwargs)

    def assertRaisesRegex(self, *args, **kwargs):
        return self._curtest.assertRaisesRegex(*args, **kwargs)

    def assertRegex(self, *args, **kwargs):
        return self._curtest.assertRegex(*args, **kwargs)

    def assertRegex(self, *args, **kwargs):
        return self._curtest.assertRegex(*args, **kwargs)

    def assertCountEqual(self, *args, **kwargs):
        return self._curtest.assertCountEqual(*args, **kwargs)

    def skipTest(self, *args, **kwargs):
        return self._curtest.skipTest(*args, **kwargs)

    def subTest(self, *args, **kwargs):
        return self._curtest.subTest(*args, **kwargs)

    def run(self, deps, tools):
        testsuite = ut.TestSuite()
        for test in self._get_test_names():
            if self.pattern.is_unset() or fnmatch.fnmatch(test, str(self.pattern)):
                testfunc = getattr(self, test)
                testsuite.addTest(
                    _TestCase(self, deps, tools, testfunc))
        with log.stream() as logstream:
            self.testresult = ut.TextTestRunner(resultclass=_TestResult, stream=logstream, verbosity=2).run(testsuite)

        raise_task_error_if(
            not self.testresult.wasSuccessful(), self,
            "{} tests out of {} were successful".format(
                len(self.testresult.successes),
                self.testresult.testsRun))



@ArtifactAttributeSetProvider.Register
class ResourceAttributeSetProvider(ArtifactAttributeSetProvider):
    def create(self, artifact):
        pass

    def parse(self, artifact, content):
        pass

    def format(self, artifact, content):
        pass

    def apply(self, task, artifact):
        task = artifact.get_task()
        if isinstance(task, Resource):
            deps = task._run_env
            deps.__enter__()
            task.acquire(artifact, deps, artifact.tools)

    def unapply(self, task, artifact):
        task = artifact.get_task()
        if isinstance(task, Resource):
            env = task._run_env
            task.release(artifact, env, artifact.tools)
            env.__exit__(None, None, None)
