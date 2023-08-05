import pytest

from wsit.main.pyx.xml.rpc.holders.array_holder import ArrayHolder


class TestArrayHolder:
    valid_values = [["value"], ["1", None, None, "str1", "str2", ""], ["1", None, "str1", None, "str2", ""],
                    [None, "1", "str1", "str2", "", None], [None, "1", "str1", "str2", ""], ["1", "str1", "str2", None],
                    ["1", "str1", None, "str2", ""], ["1", "str1", "str2", ""], ['a'], ["b"], [''], [""],

                    [True], [False], [False, True, None], [None, True, False], [False, None, True],
                    [False, None, None, True], [False, None, True, None, False], [None, False, True, None, False],
                    [None, False, True, False, None],

                    ["True"], ["False"], ["False", "True", None], [None, "True", "False"], ["False", None, "True"],
                    ["False", None, None, "True"], ["False", None, "True", None, "False"],
                    [None, "False", "True", None, "False"], [None, "False", "True", "False", None],

                    ["0"], ["1"], [None, "1", "0"], ["1", "0", None], ["1", None, "0"], [None, "1", "0", None],
                    ["1", None, None, "0"], ["1", None, "1", None, "0"],

                    [234.890], [-7389457908.39485797], [-3.14, None, 34535.45345],

                    [None], ["None"], ['None'], ["None", None, 'None'], ["None", 'None', None], [None, 'None', None],

                    [-123, 0, 1000, -32567], [None, 0, 1000, -32567], [-123, None, 1000, -32567], [-123, 0, 1000, None],
                    [-123, None, 1000, None, -32567],

                    [None, "asdfg", "1000", "-32567"], ["asdfg", None, "1000", "-32567"], ["asdfg", "1000", "-32567", None],
                    [None, None, "asdfg", "1000", "-32567"], [None, "asdfg", None, "1000", "-32567"]]

    exception_values = [[None, -123, None, 123.123, 1000, ''], ["-123", True, 1000, '', "text"], "value", 'string', 'a',
                        "b", '', "", True, False, "True", "False", "0", "1", '0', '1', 234.890, -7389457908.39485797,
                        '124.9090798', '-0.126155', 2347856247, -589578957]

    def test_init(self):
        array_holder = ArrayHolder()
        assert array_holder.get() is None

    def test_set(self):
        array_holder = ArrayHolder()
        for tested_value in TestArrayHolder.valid_values:
            array_holder.set(tested_value)
            assert array_holder.get() == tested_value

    def test_init_param(self):
        for tested_value in TestArrayHolder.valid_values:
            array_holder = ArrayHolder(tested_value)
            assert tested_value == array_holder.get()

    def test_init_exception(self):
        for tested_value in TestArrayHolder.exception_values:
            with pytest.raises(Exception):
                array_holder = ArrayHolder(tested_value)

    def test_private_field(self):
        array_holder = ArrayHolder()
        with pytest.raises(AttributeError):
            array_holder.value = 123