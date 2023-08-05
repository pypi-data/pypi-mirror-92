import pytest

from wsit.main.pyx.xml.rpc.holders.byte_holder import ByteHolder


class TestByteHolder:
    exception_values = [ByteHolder.MIN_VALUE - 1, ByteHolder.MAX_VALUE + 1, "value", 'string', 'a', "b", '', "",
                        True, False, "True", "False", "0", "1", '0', '1', 234.890, -7389457908.39485797, '124.9090798',
                        '-0.126155', "-803485.9457897", "4564690846908.4059680458960", "485739857", "-4573875937",
                        None, "None", 'None', "-67", "12", '-78', '45']
    exception_text_values = [126, -56, "value", 'string', 'a', "b", '', "", True, False, "True", "False", 234.890,
                             -7389457908.39485797, '124.9090798', '-0.126155', "-803485.9457897",
                             "4564690846908.4059680458960", "-4573875937", "8857349", None, "None", 'None']
    valid_values = [ByteHolder.MIN_VALUE, ByteHolder.MAX_VALUE, 123, -78, ByteHolder.MIN_VALUE + 1,
                    ByteHolder.MAX_VALUE - 1]

    def test_init(self):
        byte_holder = ByteHolder()
        assert byte_holder.get() == 0

    def test_init_param(self):
        for tested_value in TestByteHolder.valid_values:
            byte_holder = ByteHolder(tested_value)
            assert byte_holder.get() == tested_value

    def test_init_exception(self):
        for tested_value in TestByteHolder.exception_values:
            with pytest.raises(Exception):
                byte_holder = ByteHolder(tested_value)

    def test_private_field(self):
        byte_holder = ByteHolder()
        with pytest.raises(AttributeError):
            byte_holder.value = 123

    def test_to_string(self):
        for tested_value in TestByteHolder.valid_values:
            byte_holder = ByteHolder(tested_value)
            assert byte_holder.__str__().__eq__(str(tested_value))

    def test_equals(self):
        byte_holder_1 = ByteHolder()
        byte_holder_2 = ByteHolder()
        assert byte_holder_1.__eq__(None) is False
        assert byte_holder_1.__eq__(int("123")) is False
        assert byte_holder_1.__eq__(byte_holder_1) is True
        assert byte_holder_1.__eq__(byte_holder_2) is True
        byte_holder_2.set(123)
        assert byte_holder_1.__eq__(byte_holder_2) is False
