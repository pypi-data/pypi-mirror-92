"""
Module that contains a decorator generator function ``condition`` that
can be used to conditionally execute functions based on the state of the
global config.

General Example
---------------
Here's an example::

    from pyppy.conditions import Exp, condition
    from pyppy.config import initialize_config
    import types

    args = types.SimpleNamespace()
    args.debug = False
    initialize_config(args)

    @condition(Exp(debug=True))
    def debug_log():
        print("hello")

    debug_log() # will NOT print "hello"


Here's how it works. First, we initialize a global config with
``initialize_config``, so that executing ``config().debug`` will return
``False``.

Next, we create a function ``debug_log`` that we only want to be
executed when the value of the attribute ``debug`` in the global config
is ``True``.

To accomplish this task, we use the decorator generator ``@condition``.
It expects a function that returns a ``bool`` value when it is executed.
You can use a ``pyppy.conditions.Exp`` object (object which represents an
'expression') or a custom function (this will be explained below). In this
case, we are using a simple ``Exp`` object. The expression ``Exp(debug=True)``
means: return ``True`` when the value of the attribute ``debug`` in the global
config is ``True`` otherwise return ``False``. You can also use other types
in ``Exp`` objects like strings: ``Exp(debug="yes")`` would return
``True`` when the attribute ``debug`` in the global config is equals to "yes".

Because we set ``debug`` to ``False`` in the global config, executing
``debug_log()`` will not print anything.

Note
----
The specified condition gets evaluated when a decorated function is executed
and not when a function is defined. The decision, whether a function is executed,
can therefore change during runtime based on the state of the config. We know
that a config is usually stateless but as we do not have a stateful alternative
yet, you might have cases where you want to use config as a changing object
during runtime. (We're working on it...)


Custom Function Example
-----------------------
The logic of using ``Exp`` with keyword arguments is quite limited, as it will
always only check the exact value of the given attribute. There are many
occasions where more logic is necessary. For this reason, you can pass a
custom function to the init method of an ``Exp`` object.

Here's an example::

    from pyppy.conditions import Exp, condition
    from pyppy.config import initialize_config
    import types

    args = types.SimpleNamespace()
    args.log_level = "WARN_LEVEL_1"

    initialize_config(args)

    exp = Exp(lambda config: config.log_level.startswith("WARN"))

    @condition(exp)
    def log_warn():
        print("WARNING")

    log_warn() # will print "WARNING"

We again create a global config object. This time it has a ``log_level``
attribute. There could be multiple sub-levels for the WARN level so we
might want to check if the chosen ``log_level`` starts with ``WARN``.

This is done by passing a function to ``Exp`` which is assumed to take
the global config as the only argument and should return either ``True`` or
``False``. Based on this config object, you can implement your own logic
for returing a ``bool`` value. Here, we check if the ``log_level``
starts with an expected string. ``log_warn()`` will print ``WARNING``
because the expression returns ``True``.

We are using a lambda function here, but you can of course use a
non-anonymous function, too.

Note
----
You cannot specify both, a custom function and keyword arguments. So
you always have one of both, otherwise an exception is raised.


Logical Connection between Expressions Example
----------------------------------------------
If you have multiple expressions that you want to connect with
`and` and `or` logic, you can either write a custom function like
shown above or use the convenience methods ``and_`` and ``or_``.

Here's an example for ``and_``::

    from pyppy.conditions import condition, Exp, and_
    import types

    args = types.SimpleNamespace()
    args.log_level = "WARN"
    args.specific_log_level = "LEVEL_1"

    initialize_config(args)

    @condition(
        and_(
            Exp(log_level="WARN"),
            Exp(specific_log_level="LEVEL_1")
        )
    )
    def log_warn_level_1():
        print("WARNING LEVEL 1")

    log_warn_level_1()

The condition will only execute the function if both
expressions evaluate to ``True``.

``or_`` works similarly.

``and_`` and ``or_`` can be nested::

    and_(
        or_(
            Exp(a="b"),
            Exp(b="c")
        ),
        Exp(d="e")
    )

"""

import functools
from typing import Callable
from typing import Any

from pyppy.config import config
from pyppy.exc import ConditionRaisedException, ConditionDidNotReturnBooleansException
from pyppy.utils import _check_is_bool


def _evaluate_condition_func(single_condition: Callable[[object], bool]) -> bool:
    """
    Evaluates a condition function based on the state
    of the global config.
    """

    try:
        conf_value = single_condition(config())
    except Exception as exc:  # pylint: disable=W0703
        raise ConditionRaisedException from exc

    if _check_is_bool(conf_value):
        return conf_value

    raise ConditionDidNotReturnBooleansException(
        "The condition did not return a valid boolean!"
    )


class Exp:  # pylint: disable=R0903
    """
    Class that represents a boolean logic based on the global
    config. On creation, a condition or keyword arguments are
    given (mutually exclusive). When an instantiated object of this
    class is called, the boolean logic is evaluate.

    Parameters
    ----------
    condition_func : Callable
        A function expecting exactly one parameter which
        is the global config and returns a boolean value when it is
        called. Mutually exclusive with the ``kwargs`` parameter.
    kwargs :
        Keyword argument representing an exact match between the
        given value for the argument and the value of the corresponding attribute
        in the global config. For example, specifying ``debug="WARN"`` as keyword
        argument means that calling this object should return ``True`` when the
        value of the attribute ``debug`` in the global config is ``True``.
        Only EXACTLY ONE keyword argument is allowed. Mutually exclusive
        with the parameter ``condition_func``.

    Examples
    --------
    >>> from pyppy.config import initialize_config, destroy_config
    >>> from types import SimpleNamespace
    >>> from pyppy.config import config
    >>> destroy_config()
    >>> c = SimpleNamespace()
    >>> c.log_level = "WARN"
    >>> initialize_config(c)
    >>> config().log_level
    'WARN'

    >>> exp = Exp(log_level="WARN")
    >>> exp()
    True

    >>> exp = Exp(log_level="INFO")
    >>> exp()
    False

    >>> exp = Exp(condition_func=lambda c: c.log_level == "WARN")
    >>> exp()
    True

    >>> exp = Exp(condition_func=lambda c: c.log_level == "INFO")
    >>> exp()
    False
    """

    def __init__(self, condition_func=None, **kwargs):
        self._single_condition = condition_func
        self._kwargs = kwargs

    def __call__(self):
        if self._single_condition:
            return _evaluate_condition_func(self._single_condition)

        if len(self._kwargs) > 1:
            raise Exception("Only one key value pair allowed")
        key, val = list(self._kwargs.items())[0]

        if not hasattr(config(), key):
            return False

        if getattr(config(), key) is val:  # pylint: disable=R1703
            return True

        return False


def condition(exp: Callable[[], bool]) -> Callable[[Any], Any]:
    """
    Returns a function decorator that will evaluate the given expression
    ``exp`` when the decorated function is called. Only if the expression
    returns ``True`` the decorated function is executed.

    Parameters
    ----------
    exp : Callable
        A callable that returns ``True`` or ``False`` when called. You can
        pass whatever function you like but in the context of `pyppy` the
        function will almost always be dependent on the state of the
        global config object.
    Returns
    -------
    Callable:
        A decorator that will only execute a function if calling ``exp``
        returns ``True``.

    Examples
    --------
    >>> from pyppy.conditions import Exp, condition
    >>> from pyppy.config import initialize_config, destroy_config
    >>> import types

    >>> destroy_config()
    >>> args = types.SimpleNamespace()
    >>> args.log_level = "WARN_LEVEL_1"
    >>> initialize_config(args)

    >>> @condition(Exp(lambda c: c.log_level.startswith("WARN")))
    ... def log_warn():
    ...     print("WARNING")

    >>> log_warn()
    WARNING

    >>> @condition(Exp(log_level="WARN_LEVEL_1"))
    ... def log_warn():
    ...     print("WARNING")

    >>> log_warn()
    WARNING

    """

    def condition_decorator(func):
        """
        Decorates a function and will evaluate the expression that has
        been given to the 'condition' function.
        """
        condition_decorator.exp = exp

        @functools.wraps(func)
        def condition_check(*args, **kwargs):
            condition_result = condition_decorator.exp()

            if condition_result:
                return func(*args, **kwargs)

            return None

        return condition_check

    return condition_decorator


def and_(*exps: Callable[[], bool]) -> Callable[[], bool]:
    """
    Represents the logical conjunction between two expressions of
    type ``Exp``.

    Parameters
    ----------
    *exps: Callable
        Any number of callables without parameters that return a
        boolean value when called. The logical conjunction between
        the truth values of the called expressions will determine the
        final boolean value.

    Returns
    -------
    bool:
        The logical conjunction between the boolean values obtained
        after calling all input expressions.

    Examples
    --------
    >>> from pyppy.conditions import Exp, condition
    >>> from pyppy.config import initialize_config, destroy_config
    >>> import types

    >>> destroy_config()
    >>> args = types.SimpleNamespace()
    >>> args.log_level = "WARN"
    >>> args.specific_log_level = "LEVEL_1"
    >>> initialize_config(args)

    >>> @condition(
    ...     and_(
    ...         Exp(log_level="WARN"),
    ...         Exp(specific_log_level="LEVEL_1"),
    ...     )
    ... )
    ... def log_warn_level_1():
    ...     return "WARNING_LEVEL_1"

    >>> log_warn_level_1()
    'WARNING_LEVEL_1'
    """

    def and_evaluator():
        for exp in exps:
            current = exp()
            if not current:
                return False
        return True

    return and_evaluator


def or_(*exps: Callable[[], bool]) -> Callable[[], bool]:
    """
    Represents the logical disjunction between two expressions of
    type ``Exp``.

    Parameters
    ----------
    *exps: Callable
        Any number of callables without parameters that return a
        boolean value when called. The logical disjunction between
        the truth values of the called expressions will determine the
        final boolean value.

    Returns
    -------
    bool:
        The logical disjunction between the boolean values obtained
        after calling all input expressions.

    Examples
    --------
    >>> from pyppy.conditions import Exp, condition
    >>> from pyppy.config import initialize_config, destroy_config
    >>> import types

    >>> destroy_config()
    >>> args = types.SimpleNamespace()
    >>> args.log_level = "WARN"
    >>> initialize_config(args)

    >>> @condition(
    ...     or_(
    ...         Exp(log_level="WARN"),
    ...         Exp(log_level="INFO"),
    ...     )
    ... )
    ... def log_debug():
    ...     return "WARNING_OR_INFO"

    >>> log_debug()
    'WARNING_OR_INFO'
    """

    def or_evaluator():
        for exp in exps:
            if exp():
                return True
        return False

    return or_evaluator
