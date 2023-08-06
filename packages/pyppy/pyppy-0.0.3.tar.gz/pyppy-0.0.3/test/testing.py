from contextlib import contextmanager
from argparse import Namespace

from pyppy.config import destroy_config, initialize_config


def _fake_config(**kwargs):
    destroy_config()

    namespace = Namespace()
    for k, v in kwargs.items():
        setattr(namespace, k, v)

    initialize_config(namespace)


@contextmanager
def fake_config(**kwargs):
    _fake_config(**kwargs)

    try:
        yield
    finally:
        destroy_config()


def create_pipeline_input_function(pipeline_name, func_name, step_name=None, val=None):

    func_def = (f"@step(\"{pipeline_name}\"{',' if step_name else ''} \"{step_name}\")"
                f"\ndef {func_name}():")
    if val is not None:
        func_def += f"\n    print({val})"

        func_def += f"\n    return({val})"

    if val is None:
        func_def += "    pass"

    exec(func_def)
    return eval(func_name)
