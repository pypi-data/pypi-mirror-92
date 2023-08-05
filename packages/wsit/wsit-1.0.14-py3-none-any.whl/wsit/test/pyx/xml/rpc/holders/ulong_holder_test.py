import pytest

from wsit.main.pyx.xml.rpc.holders.ulong_holder import ULongHolder


class TestULongHolder:
    exception_values = [ULongHolder.MIN_VALUE - 1, ULongHolder.MAX_VALUE + 1, "value", 'string', 'a', "b", '', "", True,
                        False, "True", "False", "0", "1", '0', '1', -8456386589084563865890, 928374.09748724, -0.000046537658736,
                        '124.9090798', -45350.74658376578, '-0.126155', "-803485.9457897", -1,
                        "4564690846908.4059680458960", "485739857485739857485739857", "-45738759374573875937", None, "None", 'None']
    exception_text_values = [ULongHolder.MIN_VALUE - 1, ULongHolder.MAX_VALUE + 1, "value", 'string', 'a', "b", '', "",
                             True, False, "True", "False", -8456386589084563865890, 928374.09748724, -0.000046537658736,
                             '124.9090798', -45350.74658376578, '-0.126155', "-803485.9457897",
                             "4564690846908.4059680458960", "485739857485739857485739857", "-457387593745738759374573875937", None, "None", 'None']
    valid_values = [ULongHolder.MIN_VALUE, ULongHolder.MAX_VALUE, 123456789012345678, ULongHolder.MIN_VALUE + 1,
                    ULongHolder.MAX_VALUE - 1]

    def test_init(self):
        ulong_holder = ULongHolder()
        assert ulong_holder.get() == 0

    def test_init_param(self):
        for tested_value in TestULongHolder.valid_values:
            ulong_holder = ULongHolder(tested_value)
            assert ulong_holder.get() == tested_value

    def test_init_exception(self):
        for tested_value in TestULongHolder.exception_values:
            with pytest.raises(Exception):
                ulong_holder = ULongHolder(tested_value)

    def test_private_field(self):
        ulong_holder = ULongHolder()
        with pytest.raises(AttributeError):
            ulong_holder.value = 123

    def test_to_string(self):
        for tested_value in TestULongHolder.valid_values:
            ulong_holder = ULongHolder(tested_value)
            assert ulong_holder.__str__().__eq__(str(tested_value))

    def test_equals(self):
        ulong_holder_1 = ULongHolder()
        ulong_holder_2 = ULongHolder()
        assert ulong_holder_1.__eq__(None) is False
        assert ulong_holder_1.__eq__(int("123")) is False
        assert ulong_holder_1.__eq__(ulong_holder_1) is True
        assert ulong_holder_1.__eq__(ulong_holder_2) is True
        ulong_holder_2.set(123456789012345678)
        assert ulong_holder_1.__eq__(ulong_holder_2) is False
