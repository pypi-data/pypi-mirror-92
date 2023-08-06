from pyppy.args import fill_arguments
from pyppy.config import destroy_config, initialize_config
from pyppy.exc import FunctionSignatureNotSupportedException, OnlyKeywordArgumentsAllowedException, \
    ConflictingArgumentValuesException, IllegalStateException
from test.testcase import TestCase
from test.testing import fake_config

DEFAULT_ARG_DICT = {
    "arg1": "val1",
    "arg2": "val2",
    "arg3": "val3",
    "arg4": "val4"
}

MIXED_TYPE_ARG_DICT = {
    "arg1": "1",
    "arg2": 2,
    "arg3": (3,),
    "arg4": {4: 4}
}

DEFAULT_CONT_DICT = {
    "cont1": "cval1",
    "cont2": "cval2",
    "cont3": "cval3",
    "cont4": "cval4"
}


class FillArgumentsTest(TestCase):

    def setUp(self) -> None:
        destroy_config()

    def test_fill_one_arg(self):
        with fake_config(**DEFAULT_ARG_DICT):
            @fill_arguments()
            def tmp(arg1):
                return arg1

            self.assertEqual(tmp(), DEFAULT_ARG_DICT['arg1'])

    def test_fill_two_args(self):
        with fake_config(**DEFAULT_ARG_DICT):
            @fill_arguments()
            def tmp(arg1, arg2):
                return arg1, arg2

            self.assertEqual(tmp(), (DEFAULT_ARG_DICT['arg1'],
                                     DEFAULT_ARG_DICT['arg2']))

    def test_fill_outer_args(self):
        with fake_config(**DEFAULT_ARG_DICT):
            @fill_arguments("arg1", "arg3")
            def tmp(arg1, arg2, arg3):
                return arg1, arg2, arg3

            self.assertEqual(
                tmp(arg2=DEFAULT_ARG_DICT['arg2']),
                (DEFAULT_ARG_DICT['arg1'],
                 DEFAULT_ARG_DICT['arg2'],
                 DEFAULT_ARG_DICT['arg3']))

    def test_fill_nonexistent_config_param(self):
        with fake_config(**DEFAULT_ARG_DICT):
            @fill_arguments()
            def tmp(arg1, tmp_arg, arg3):
                return arg1, tmp_arg, arg3

            self.assertEqual(
                tmp(tmp_arg=DEFAULT_ARG_DICT['arg2']),
                (DEFAULT_ARG_DICT['arg1'],
                 DEFAULT_ARG_DICT['arg2'],
                 DEFAULT_ARG_DICT['arg3']))

    def test_fill_positional_arg(self):
        with fake_config(**DEFAULT_ARG_DICT):
            @fill_arguments("arg3")
            def tmp2(arg3, arg4="blabla"):
                return arg3, arg4
            self.assertEqual(tmp2(), (
                DEFAULT_ARG_DICT['arg3'],
                "blabla"
            ))
            self.assertEqual(tmp2(arg4="cool"), (
                DEFAULT_ARG_DICT['arg3'],
                "cool"
            ))

    def test_fill_keyword_arg(self):
        with fake_config(**DEFAULT_ARG_DICT):
            @fill_arguments("arg4")
            def tmp3(arg3, arg4="blabla"):
                return arg3, arg4

            self.assertEqual(tmp3(arg3="cool"), (
                "cool",
                DEFAULT_ARG_DICT['arg4']
            ))

    def test_fill_keyword_arg_2(self):
        with fake_config(**DEFAULT_ARG_DICT):
            @fill_arguments("arg4")
            def tmp4(arg3="tmp", arg4="blabla"):
                return arg3, arg4

            self.assertEqual(tmp4(arg3="cool"), (
                "cool",
                "val4"
            ))

    def test_fill_correct_types(self):
        with fake_config(**MIXED_TYPE_ARG_DICT):
            @fill_arguments()
            def tmp(arg1, arg2, arg3, arg4):
                return arg1, arg2, arg3, arg4

            result = tmp()
            self.assertIsInstance(result[0], str)
            self.assertIsInstance(result[1], int)
            self.assertIsInstance(result[2], tuple)
            self.assertIsInstance(result[3], dict)

    def test_overwrite_defaults(self):
        with fake_config(**DEFAULT_ARG_DICT):
            @fill_arguments()
            def tmp(arg1="tmp1", arg2="tmp2", arg3="tmp3", arg4="tmp4"):
                return arg1, arg2, arg3, arg4

            self.assertEqual(tmp(), (
                DEFAULT_ARG_DICT['arg1'],
                DEFAULT_ARG_DICT['arg2'],
                DEFAULT_ARG_DICT['arg3'],
                DEFAULT_ARG_DICT['arg4']
            ))

    def test_positional_args_raise(self):
        with fake_config(**DEFAULT_ARG_DICT):
            @fill_arguments()
            def tmp(arg1, arg2="tmp"):
                return arg1, arg2

            with self.assertRaises(
                OnlyKeywordArgumentsAllowedException
            ):
                tmp("tmp")

    def test_overwrite_filled_arguments(self):
        with fake_config(**DEFAULT_ARG_DICT):
            @fill_arguments()
            def tmp(arg1="tmp1", arg2="tmp2", arg3="tmp3", arg4="tmp4"):
                return arg1, arg2, arg3, arg4

            self.assertEqual(tmp(
                arg1="hurz1", arg2="hurz2", arg3="hurz3", arg4="hurz4"
            ), (
                "hurz1", "hurz2", "hurz3", "hurz4"
            ))

    def test_raise_positional_only_args(self):
        with fake_config(**DEFAULT_ARG_DICT):
            with self.assertRaises(FunctionSignatureNotSupportedException):
                @fill_arguments("arg3", "arg4")
                def tmp4(x, y, /, arg3, arg4="blabla"):
                    return x, y, arg3, arg4

    def test_raise_keyword_only(self):
        with fake_config(**DEFAULT_ARG_DICT):
            with self.assertRaises(FunctionSignatureNotSupportedException):
                @fill_arguments()
                def tmp4(arg1, *args, arg4="blabla"):
                    return arg1, args, arg4

    def test_raise_var_keyword(self):
        with fake_config(**DEFAULT_ARG_DICT):
            with self.assertRaises(FunctionSignatureNotSupportedException):
                @fill_arguments()
                def tmp4(arg1, **kwargs):
                    return arg1, kwargs
