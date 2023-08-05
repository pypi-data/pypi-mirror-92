import pytest

from wsit.main.pyx.xml.rpc.holders.ushort_holder import UShortHolder


class TestUShortHolder:
    exception_values = [UShortHolder.MIN_VALUE-1, UShortHolder.MAX_VALUE+1, "value", 'string', 'a', "b", '', "",
                        True, False, "True", "False", "0", "1", '0', '1', 234.890, -7389457908.39485797, '124.9090798',
                        '-0.126155', "-803485.9457897", "4564690846908.4059680458960", "485739857", "-4573875937",
                        None, "None", 'None']
    exception_text_values = [str(UShortHolder.MIN_VALUE-1), str(UShortHolder.MAX_VALUE+1), "value", 'string', 'a', "b",
                             '', "", True, False, "True", "False", 234.890, -7389457908.39485797, '124.9090798',
                             '-0.126155', "-803485.9457897", "4564690846908.4059680458960", "-4573875937", "8857349",
                             None, "None", 'None']
    valid_values = [UShortHolder.MIN_VALUE, UShortHolder.MAX_VALUE, 12345, UShortHolder.MIN_VALUE + 1,
                    UShortHolder.MAX_VALUE - 1]

    def test_init(self):
        ushort_holder = UShortHolder()
        assert ushort_holder.get() == 0

    def test_init_param(self):
        for tested_value in TestUShortHolder.valid_values:
            ushort_holder = UShortHolder(tested_value)
            assert ushort_holder.get() == tested_value

    def test_init_exception(self):
        for tested_value in TestUShortHolder.exception_values:
            with pytest.raises(Exception):
                ushort_holder = UShortHolder(tested_value)

    def test_private_field(self):
        ushort_holder = UShortHolder()
        with pytest.raises(AttributeError):
            ushort_holder.value = 123

    def test_to_string(self):
        for tested_value in TestUShortHolder.valid_values:
            ushort_holder = UShortHolder(tested_value)
            assert ushort_holder.__str__().__eq__(str(tested_value))

    def test_equals(self):
        ushort_holder_1 = UShortHolder()
        ushort_holder_2 = UShortHolder()
        assert ushort_holder_1.__eq__(None) is False
        assert ushort_holder_1.__eq__(int("123")) is False
        assert ushort_holder_1.__eq__(ushort_holder_1) is True
        assert ushort_holder_1.__eq__(ushort_holder_2) is True
        ushort_holder_2.set(12345)
        assert ushort_holder_1.__eq__(ushort_holder_2) is False
