import pytest

from wsit.main.pyx.xml.rpc.holders.ubyte_holder import UByteHolder


class TestUByteHolder:
    exception_values = [UByteHolder.MIN_VALUE - 1, UByteHolder.MAX_VALUE + 1, "value", 'string', 'a', "b", '', "",
                        True, False, "True", "False", "0", "1", '0', '1', 234.890, -7389457908.39485797, '124.9090798',
                        '-0.126155', "-803485.9457897", "4564690846908.4059680458960", "485739857", "-4573875937",
                        None, "None", 'None']
    exception_text_values = [str(UByteHolder.MIN_VALUE - 1), str(UByteHolder.MAX_VALUE + 1), "value", 'string', 'a', "b",
                             '', "", True, False, "True", "False", 234.890, -7389457908.39485797, '124.9090798',
                             '-0.126155', "-803485.9457897", "4564690846908.4059680458960", "-4573875937", "8857349",
                             None, "None", 'None']
    valid_values = [UByteHolder.MIN_VALUE, UByteHolder.MAX_VALUE, 123, UByteHolder.MIN_VALUE + 1,
                    UByteHolder.MAX_VALUE - 1]

    def test_init(self):
        ubyte_holder = UByteHolder()
        assert ubyte_holder.get() == 0

    def test_private_field(self):
        ubyte_holder = UByteHolder()
        with pytest.raises(AttributeError):
            ubyte_holder.value = 123

    def test_init_param(self):
        for tested_value in TestUByteHolder.valid_values:
            ubyte_holder = UByteHolder(tested_value)
            assert ubyte_holder.get() == tested_value

    def test_init_exception(self):
        for tested_value in TestUByteHolder.exception_values:
            with pytest.raises(Exception):
                ubyte_holder = UByteHolder(tested_value)

    def test_to_string(self):
        for tested_value in TestUByteHolder.valid_values:
            ubyte_holder = UByteHolder(tested_value)
            assert ubyte_holder.__str__().__eq__(str(tested_value))

    def test_equals(self):
        short_holder_1 = UByteHolder()
        short_holder_2 = UByteHolder()
        assert short_holder_1.__eq__(None) is False
        assert short_holder_1.__eq__(int("123")) is False
        assert short_holder_1.__eq__(short_holder_1) is True
        assert short_holder_1.__eq__(short_holder_2) is True
        short_holder_2.set(45)
        assert short_holder_1.__eq__(short_holder_2) is False
