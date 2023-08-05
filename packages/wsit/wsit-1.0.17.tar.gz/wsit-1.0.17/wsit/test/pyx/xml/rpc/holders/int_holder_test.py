import pytest

from wsit.main.pyx.xml.rpc.holders.int_holder import IntHolder


class TestIntHolder:
    exception_values = [IntHolder.MIN_VALUE - 1, IntHolder.MAX_VALUE + 1, "value", 'string', 'a', "b", '', "", True,
                        False, "True", "False", "0", "1", '0', '1', -84563865890, 928374.09748724, -0.000046537658736,
                        '124.9090798', -45350.74658376578, '-0.126155', "-803485.9457897",
                        "4564690846908.4059680458960", "485739857", "-4573875937", None, "None", 'None']
    exception_text_values = [IntHolder.MIN_VALUE - 1, IntHolder.MAX_VALUE + 1, "value", 'string', 'a', "b", '', "",
                             True, False, "True", "False", -845638658, 928374.09748724, -0.000046537658736,
                             '124.9090798', -45350.74658376578, '-0.126155', "-803485.9457897",
                             "4564690846908.4059680458960", "485739857987", "-4573875937", None, "None", 'None']
    valid_values = [IntHolder.MIN_VALUE, IntHolder.MAX_VALUE, 1234567890, IntHolder.MIN_VALUE + 1,
                    IntHolder.MAX_VALUE - 1]

    def test_init(self):
        int_holder = IntHolder()
        assert int_holder.get() == 0

    def test_init_param(self):
        for tested_value in TestIntHolder.valid_values:
            int_holder = IntHolder(tested_value)
            assert int_holder.get() == tested_value

    def test_init_exception(self):
        for tested_value in TestIntHolder.exception_values:
            with pytest.raises(Exception):
                int_holder = IntHolder(tested_value)

    def test_private_field(self):
        int_holder = IntHolder()
        with pytest.raises(AttributeError):
            int_holder.value = 123

    def test_to_string(self):
        for tested_value in TestIntHolder.valid_values:
            int_holder = IntHolder(tested_value)
            assert int_holder.__str__().__eq__(str(tested_value))

    def test_equals(self):
        int_holder_1 = IntHolder()
        int_holder_2 = IntHolder()
        assert int_holder_1.__eq__(None) is False
        assert int_holder_1.__eq__(int("123")) is False
        assert int_holder_1.__eq__(int_holder_1) is True
        assert int_holder_1.__eq__(int_holder_2) is True
        int_holder_2.set(123456)
        assert int_holder_1.__eq__(int_holder_2) is False
