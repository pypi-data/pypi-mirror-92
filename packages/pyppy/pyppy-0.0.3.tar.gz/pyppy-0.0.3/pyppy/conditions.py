import functools

from pyppy.config import config
from pyppy.exc import AmbiguousConditionValuesException, ConditionRaisedException, \
    ConditionDidNotReturnBooleansException


def and_(*args):
    def inner():
        for arg in args:
            current = arg()
            if not current:
                return False
        return True
    return inner


def or_(*args):
    def inner():
        for arg in args:
            if arg():
                return True
        return False
    return inner


def _check_bool(value):
    if isinstance(value, bool):
        return True
    else:
        return False


def evaluate_single_condition(single_condition):
    exceptions = []

    try:
        conf_value = single_condition(config())
    except Exception as e1:
        exceptions.append(e1)
        conf_value = None

    if conf_value is None:
        raise ConditionRaisedException(exceptions)
    else:
        if _check_bool(conf_value):
            return conf_value

    raise ConditionDidNotReturnBooleansException(
        "The condition did not return a valid boolean!"
    )


def exp(single_condition=None, **kwargs):
    def condition_evaluator():
        if single_condition:
            return evaluate_single_condition(single_condition)

        if len(kwargs) > 1:
            raise Exception(
                "Only one key value pair allowed"
            )
        k, v = list(kwargs.items())[0]

        if not hasattr(config(), k):
            return False

        if getattr(config(), k) is v:
            return True
        else:
            return False

    return condition_evaluator


def condition(exp):
    def condition_decorator(func):
        condition_decorator.exp = exp
        func.exp = exp

        @functools.wraps(func)
        def condition_check(*args, **kwargs):
            condition_check.exp = exp
            condition_result = condition_decorator.exp()

            if condition_result:
                return func(*args, **kwargs)
        return condition_check
    return condition_decorator
