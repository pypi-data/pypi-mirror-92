from argparse import Namespace

from pyppy.exc import ConfigAlreadyInitializedException

_CONFIG = "confyg"


def initialize_config(args=Namespace()):
    if hasattr(config, _CONFIG):
        raise ConfigAlreadyInitializedException((
            "Config has already been initialized. "
            "If you want to initialize a new config call "
            f"{destroy_config.__name__}()."
        ))
    config(args)


def config(args=None):
    if not hasattr(config, _CONFIG) and args:
        setattr(config, _CONFIG, args)
    if not hasattr(config, _CONFIG):
        raise Exception("Please initialize config first!")

    return getattr(config, _CONFIG)


def destroy_config():
    if hasattr(config, _CONFIG):
        delattr(config, _CONFIG)

