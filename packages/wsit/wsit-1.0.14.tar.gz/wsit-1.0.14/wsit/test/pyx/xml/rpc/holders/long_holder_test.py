import pytest

from wsit.main.pyx.xml.rpc.holders.long_holder import LongHolder


class TestLongHolder:
    exception_values = [LongHolder.MIN_VALUE - 1, LongHolder.MAX_VALUE + 1, "value", 'string', 'a', "b", '', "", True,
                        False, "True", "False", "0", "1", '0', '1', -8456386589084563865890, 928374.09748724, -0.000046537658736,
                        '124.9090798', -45350.74658376578, '-0.126155', "-803485.9457897",
                        "4564690846908.4059680458960", "485739857485739857485739857", "-45738759374573875937", None, "None", 'None']
    exception_text_values = [LongHolder.MIN_VALUE - 1, LongHolder.MAX_VALUE + 1, "value", 'string', 'a', "b", '', "",
                             True, False, "True", "False", -8456386589084563865890, 928374.09748724, -0.000046537658736,
                             '124.9090798', -45350.74658376578, '-0.126155', "-803485.9457897",
                             "4564690846908.4059680458960", "485739857485739857485739857", "-457387593745738759374573875937", None, "None", 'None']
    valid_values = [LongHolder.MIN_VALUE, LongHolder.MAX_VALUE, 123456789012345678, LongHolder.MIN_VALUE + 1,
                    LongHolder.MAX_VALUE - 1]

    def test_init(self):
        long_holder = LongHolder()
        assert long_holder.get() == 0

    def test_init_param(self):
        for tested_value in TestLongHolder.valid_values:
            long_holder = LongHolder(tested_value)
            assert long_holder.get() == tested_value

    def test_init_exception(self):
        for tested_value in TestLongHolder.exception_values:
            with pytest.raises(Exception):
                long_holder = LongHolder(tested_value)

    def test_private_field(self):
        long_holder = LongHolder()
        with pytest.raises(AttributeError):
            long_holder.value = 123

    def test_to_string(self):
        for tested_value in TestLongHolder.valid_values:
            long_holder = LongHolder(tested_value)
            assert long_holder.__str__().__eq__(str(tested_value))

    def test_equals(self):
        long_holder_1 = LongHolder()
        long_holder_2 = LongHolder()
        assert long_holder_1.__eq__(None) is False
        assert long_holder_1.__eq__(int("123")) is False
        assert long_holder_1.__eq__(long_holder_1) is True
        assert long_holder_1.__eq__(long_holder_2) is True
        long_holder_2.set(123456789012345678)
        assert long_holder_1.__eq__(long_holder_2) is False
