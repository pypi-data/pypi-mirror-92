import pytest

from wsit.main.pyx.xml.rpc.holders.uint_holder import UIntHolder


class TestUIntHolder:
    exception_values = [UIntHolder.MIN_VALUE-1, UIntHolder.MAX_VALUE+1, "value", 'string', 'a', "b", '', "", True,
                        False, "True", "False", "0", "1", '0', '1', 234.890, -7389457908.39485797, '124.9090798',
                        '-0.126155', "-803485.9457897", "4564690846908.4059680458960", "485739857", "-4573875937",
                        None, "None", 'None', -1]
    exception_text_values = [UIntHolder.MIN_VALUE-1, UIntHolder.MAX_VALUE+1, "value", 'string', 'a', "b", '', "",
                             True, False, "True", "False", 234.890, -7389457908.39485797, '124.9090798', '-0.126155',
                             "-803485.9457897", "4564690846908.4059680458960", "-4573875937", None, "None", 'None']
    valid_values = [UIntHolder.MIN_VALUE, UIntHolder.MAX_VALUE, 123456, UIntHolder.MIN_VALUE+1, UIntHolder.MAX_VALUE-1]

    def test_init(self):
        uint_holder = UIntHolder()
        assert uint_holder.get() == 0

    def test_init_param(self):
        for tested_value in TestUIntHolder.valid_values:
            uint_holder = UIntHolder(tested_value)
            assert uint_holder.get() == tested_value

    def test_init_exception(self):
        for tested_value in TestUIntHolder.exception_values:
            with pytest.raises(Exception):
                uint_holder = UIntHolder(tested_value)

    def test_private_field(self):
        uint_holder = UIntHolder()
        with pytest.raises(AttributeError):
            uint_holder.value = 123

    def test_to_string(self):
        for tested_value in TestUIntHolder.valid_values:
            uint_holder = UIntHolder(tested_value)
            assert uint_holder.__str__().__eq__(str(tested_value))

    def test_equals(self):
        uint_holder_1 = UIntHolder()
        uint_holder_2 = UIntHolder()
        assert uint_holder_1.__eq__(None) is False
        assert uint_holder_1.__eq__(int("123")) is False
        assert uint_holder_1.__eq__(uint_holder_1) is True
        assert uint_holder_1.__eq__(uint_holder_2) is True
        uint_holder_2.set(123456)
        assert uint_holder_1.__eq__(uint_holder_2) is False
