class ConfigAlreadyInitializedException(Exception):
    pass


class MissingPipelineException(Exception):
    pass


class MissingConfigParamException(Exception):
    pass


class PipelineAlreadyExistsException(Exception):
    pass


class AmbiguousConditionValuesException(Exception):
    pass


class ConditionRaisedException(Exception):
    pass


class ConditionDidNotReturnBooleansException(Exception):
    pass


class ConflictingArgumentValuesException(Exception):
    pass


class FunctionSignatureNotSupportedException(Exception):
    pass


class OnlyKeywordArgumentsAllowedException(Exception):
    pass


class IllegalStateException(Exception):
    pass
