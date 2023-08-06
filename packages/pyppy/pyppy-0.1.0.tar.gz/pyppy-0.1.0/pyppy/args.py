"""Automatic Argument Filling from Config

Contains a decorator generator that allows to automatically fill
function arguments based on attributes of the global config created
with ``initialize_config(obj)``.

General Example
---------------
Sounds too abstract? Here's an example::

    from argparse import ArgumentParser
    from pyppy.args import fill_args
    from pyppy.config import initialize_config

    parser = ArgumentParser()
    parser.add_argument(
        "--debug",
        action="store_true",
        default=False
    )

    cli_args = ["--debug"]
    args = parser.parse_args(cli_args)

    initialize_config(args)


    @fill_args()
    def log_debug(debug, message):
        if debug is True:
            print(message)


    log_debug(message="debugging")
    # will print "debugging"

Let's go through the example step by step. First, we define an
``ArgumentParser`` which can read in some arguments and parse them.
In this case, we have an argument `--debug` which will, when specified,
be ``True`` otherwise ``False``. The ``ArgumentParser`` will return
an ``argparse.Namespace`` object that holds an attribute ``debug``
with the corresponding value.

Then, we initialize our config with the returned ``Namespace`` object.
This will register a global config that we can access by calling
``pyppy.config.config()``. So, calling ``config().debug``
will result in ``True``.


After that, we
define a function and tell it to automatically fill its arguments based
on the attributes of the global configuration we just registered. For
this, we use the decorator generator ``fill_args`` that will, when called,
return a function generator able to fill the arguments of the function.
It will look for parameters in the function's definition that have the
same name as attributes of the global config. In this case we have
an exact match between ``debug`` in the function parameters and the
global configuration attribute ``debug``. So, when executing the function
``log_debug`` we don't have to provide debug because it has already assigned
an value equal to the attribute's value in the global config.```

When calling ``log_debug``, we have to provide the ``message`` argument
as keyword argument (this is currently necessary; we're working on
allowing positional parameters too...). That's it. You can use this
for whatever parameters you want to be filled from the global config.

Explicit Argument Filling
-------------------------

There are cases where you might not want ``fill_args``  to
automatically detect the arguments to be filled for you. In these
cases, you can tell ``fill_args`` explicitly which arguments you
want to fill from the config::

    @fill_args("debug")
    def log_debug(debug, message):
        if debug is True:
            print(message)

When specifying explicitly filled arguments, only these arguments
are filled. So if there are other matching parameters they will be
left untouched. You can specify as many explicit arguments as you want;
just pass the comma-separated as strings to the ``fill_args`` method.

Note
----
    Currently only function signatures are allowed where each argument
    can be specified as keyword argument when calling the function.
    E.g. you can not use positional-only arguments when using the
    ``fill_args`` function. The following signature, for example,
    will not work: ``func(x, y, /, z, a="b")``.
"""

import functools
from inspect import signature
from typing import Callable, Any

from pyppy.config import config
from pyppy.exc import (
    FunctionSignatureNotSupportedException,
    OnlyKeywordArgumentsAllowedException,
    IllegalStateException,
)


_UNSET_VALUE = "<pyppy-unset-value>"


def _check_func_signature_supported(func: Callable) -> None:
    """
    Checks if a given function has a supported type.
    If function signature includes parameters that are
    of kind POSTIONAL_ONLY, VAR_KEYWORD or VAR_POSITIONAL
    an FunctionSignatureNotSupportedException is raised.
    """
    sig = signature(func)

    for _, param in sig.parameters.items():
        if param.kind in (
            param.POSITIONAL_ONLY,
            param.VAR_KEYWORD,
            param.VAR_POSITIONAL,
        ):
            raise FunctionSignatureNotSupportedException(
                (
                    "Currently only functions with arguments that have types "
                    "of POSITIONAL_OR_KEYWORD and KEYWORD_ONLY are supported."
                )
            )


def fill_args(*args_to_be_filled: str) -> Callable:
    """
    Returns a function decorator that automatically fills function
    arguments based on the global config object attributes. Function arguments
    that have the same name as an attribute of the global config will
    be automatically filled with the corresponding value when the
    decorated function is executed.

    Parameters
    ----------
    args_to_be_filled : str
        Varargs parameter that allows to explicitly set the arguments that
        are filled from the global configs attributes. The Decorator returned
        from ``fill_args`` will only fill the explicitly mentioned arguments
        and will leave every other argument untouched.

    Returns
    -------
    Callable :
        Wrapper around the original function that will take care of argument
        filling functionality when the decorated function is called.

    Examples
    --------
    >>> from pyppy.config import initialize_config, destroy_config
    >>> from types import SimpleNamespace
    >>> from pyppy.config import config
    >>> destroy_config()
    >>> c = SimpleNamespace()
    >>> c.debug_level = "WARN"
    >>> initialize_config(c)
    >>> config().debug_level
    'WARN'
    >>> @fill_args()
    ... def debug(debug_level, message):
    ...     if debug_level == "WARN":
    ...         return message
    >>> debug(message="WARNING!!!")
    'WARNING!!!'
    """

    def fill_args_decorator(func: Callable) -> Callable:
        """
        Function decorator that takes a function and return a new
        function that will, when executed, fill arguments of the
        original function based on their value in the global config.

        Currently specific function signatures are supported.
        The decorator checks if a function signature is supported
        and raises an exception otherwise.
        """
        _check_func_signature_supported(func)
        sig = signature(func)
        filled_kwargs = {}

        @functools.wraps(func)
        def argument_filler(*args: Any, **kwargs: Any) -> Callable:
            """
            Wrapper around the original function. This function checks
            if arguments of the original function have the same name
            as attributes of the global config.

            If the arguments to be filled have been set explicitly
            in the fill_args function only the corresponding arguments
            are checked.

            If arguments are declared a arguments to be filled but are
            not present in the global config object it is still
            possible to provide them as keyword argument on function
            execution. If the corresponding arguments are not filled
            from the config and not provided on function execution
            an exception is raised.
            """
            for name, _ in sig.parameters.items():
                if name in args_to_be_filled or len(args_to_be_filled) == 0:
                    try:
                        value = getattr(config(), name)
                    except AttributeError:
                        value = _UNSET_VALUE
                    filled_kwargs[name] = value

            if len(args) > 0:
                raise OnlyKeywordArgumentsAllowedException(
                    (
                        f"Only keyword arguments are allowed when executing a "
                        f"function defined with the {fill_args.__name__} "
                        f"decorator."
                    )
                )

            filled_kwargs.update(kwargs)

            for name, value in filled_kwargs.items():
                if value is _UNSET_VALUE:
                    raise IllegalStateException(
                        f"\n\tArgument {name} was not present in the global \n\t"
                        f"config and was not provided as keyword argument when \n\t"
                        f"the function {func} was executed. Please make sure \n\t"
                        f"needed arguments are either provided within the config \n\t"
                        f"or when running a {fill_args.__name__}-decorated function."
                    )

            return func(**filled_kwargs)

        return argument_filler

    return fill_args_decorator
