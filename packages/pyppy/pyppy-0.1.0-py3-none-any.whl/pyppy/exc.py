"""
Contains exceptions for pyppy.
"""


class ConfigAlreadyInitializedException(Exception):
    """
    Exception indicating that a global config has already
    been initialized.
    """


class MissingConfigParamException(Exception):
    """
    MissingConfigParamException
    """


class ConditionRaisedException(Exception):
    """
    ConditionRaisedException
    """


class ConditionDidNotReturnBooleansException(Exception):
    """
    ConditionDidNotReturnBooleansException
    """


class FunctionSignatureNotSupportedException(Exception):
    """
    FunctionSignatureNotSupportedException
    """


class OnlyKeywordArgumentsAllowedException(Exception):
    """
    OnlyKeywordArgumentsAllowedException
    """


class IllegalStateException(Exception):
    """
    IllegalStateException
    """
