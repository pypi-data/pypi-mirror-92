import pytest

from wsit.main.pyx.xml.rpc.holders.string_holder import StringHolder


class TestStringHolder:
    exception_values = [True, False, 234.890, -7389457908.39485797, 23784629846, -98753948, 0, 1]
    valid_values = ["value", 'string', 'a', "b", '', "", "True", "False", "0", "1", '0', '1', '124.9090798',
                    '-0.126155', "-803485.9457897", "4564690846908.4059680458960", "485739857", "-4573875937", "None",
                    'None']

    def test_init(self):
        string_holder = StringHolder()
        assert string_holder.get() is None

    def test_private_field(self):
        string_holder = StringHolder()
        with pytest.raises(AttributeError):
            string_holder.value = 123

    def test_init_param(self):
        for tested_value in TestStringHolder.valid_values:
            string_holder = StringHolder(tested_value)
            assert string_holder.get() == tested_value

    def test_init_exception(self):
        for tested_value in TestStringHolder.exception_values:
            with pytest.raises(Exception):
                string_holder = StringHolder(tested_value)

    def test_to_string(self):
        for tested_value in TestStringHolder.valid_values:
            string_holder = StringHolder(tested_value)
            assert string_holder.__str__().__eq__(tested_value)

    def test_equals(self):
        string_holder_1 = StringHolder("FirstString")
        string_holder_2 = StringHolder("FirstString")
        assert string_holder_1.__eq__(None) is False
        assert string_holder_1.__eq__(int("123")) is False
        assert string_holder_1.__eq__(string_holder_1) is True
        assert string_holder_1.__eq__(string_holder_2) is True
        string_holder_2.set("AnotherString")
        assert string_holder_1.__eq__(string_holder_2) is False
