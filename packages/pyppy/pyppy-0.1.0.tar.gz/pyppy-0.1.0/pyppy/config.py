"""Global config management

This module provides functions for initializing, accessing and destroying
a global config object. You can initialize a global config from any object.
However, in the context of pyppy, only the instance attributes of the
object are used and work with the decorators ``fill_args`` and ``condition``.
But you can use any object you like. The config management methods are
just a convenience reference to the original object.

Initialization
--------------
In this example, we initialize a global config from a ``NameSpace`` parsed
with a custom ``ArgumentParser``. For demonstration purposes, the parser
will not parse args from the commandline but from a list::

    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument("--message")

    # parse_args returns an argparse.Namespace
    args = parser.parse_args(["--message", "hello!"])

To initialize a global config object, import the function ``initialize_config``
and pass the args variable::

    from pyppy.config import initialize_config
    initialize_config(args)

You can also create an empty global object (which just holds a reference
to an empty ``object``) and change it afterwards via
accessing the global config object (see Config access section)::

    from pyppy.config import initialize_config
    initialize_config(args)

Access
------
Now that you have initialized the global config, you can use it
throughout your code::

    from pyppy.config import config
    print(config().message)
    # "hello!"

Note
----
    The original object that you used to initialize the global config
    is returned any time you call ``config()``, so you can do everything
    with the object that you could also do before.

Modification
------------
It is possible to change the global config object during time, e.g. to pass
information between objects in your code. We know that the term 'config'
is not ideal for these use cases and we're working on functionality to
handle these use cases in a better way. Here's an example of config
modification::

    config().message = "bye!"
    print(config().message)

Reset
-----
There can be only one global config object. So whenever you have
initialized a config you cannot initialize a new one. If you try to
an exception is raised. In the rare cases you might want to have
a new global config you can explicitly destroy the current one and
initialize a new one::

    from pyppy.config import destroy_config
    destroy_config()
    initialize_config(args2)

"""
from types import SimpleNamespace
from pyppy.exc import ConfigAlreadyInitializedException

_CONFIG = "pyppy-config"


def initialize_config(obj: object = SimpleNamespace()) -> None:
    """
    Initialize a global config with the specified object or
    with an empty ``object`` if no object is given.

    Parameters
    ----------
    obj : object
        Object to initialize the global config with. Whenever
        you will call ``pyppy.config.config()`` you will get a r
        reference to this object.
    Returns
    -------
    None

    Examples
    --------
    >>> destroy_config()
    >>> c = SimpleNamespace()
    >>> c.option = "say_hello"
    >>> initialize_config(c)
    >>> config().option
    'say_hello'
    >>> destroy_config()

    """
    if hasattr(config, _CONFIG):
        raise ConfigAlreadyInitializedException(
            (
                "Config has already been initialized. "
                "If you want to initialize a new config call "
                f"{destroy_config.__name__}()."
            )
        )
    config(obj)


def config(_obj: object = None) -> object:
    """
    Accesses a previously initialized global config.

    Returns
    -------
    object:
        The object that was used to initialize the global
        config.

    Examples
    --------
    >>> destroy_config()
    >>> c = SimpleNamespace()
    >>> c.option = "say_hello"
    >>> initialize_config(c)
    >>> config().option
    'say_hello'
    >>> destroy_config()
    """
    if not hasattr(config, _CONFIG) and _obj:
        setattr(config, _CONFIG, _obj)
    if not hasattr(config, _CONFIG):
        raise Exception("Please initialize config first!")

    return getattr(config, _CONFIG)


def destroy_config() -> None:
    """
    Deletes the global reference to the object that the config
    was initialized with.

    Examples
    --------
    >>> destroy_config()
    >>> c = SimpleNamespace()
    >>> c.option = "say_hello"
    >>> initialize_config(c)
    >>> config().option
    'say_hello'
    >>> destroy_config()
    >>> config().option
    Traceback (most recent call last):
    ...
    Exception: Please initialize config first!
    """
    if hasattr(config, _CONFIG):
        delattr(config, _CONFIG)
