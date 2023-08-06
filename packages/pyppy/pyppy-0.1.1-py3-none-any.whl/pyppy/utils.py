"""
Contains generally useful util functions.
"""


def _check_is_bool(value):
    if isinstance(value, bool):  # pylint: disable=R1703
        return True

    return False
