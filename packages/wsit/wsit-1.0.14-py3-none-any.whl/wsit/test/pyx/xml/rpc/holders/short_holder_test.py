import pytest

from wsit.main.pyx.xml.rpc.holders.short_holder import ShortHolder


class TestShortHolder:
    exception_values = [ShortHolder.MIN_VALUE - 1, ShortHolder.MAX_VALUE + 1, "value", 'string', 'a', "b", '', "",
                        True, False, "True", "False", "0", "1", '0', '1', 234.890, -7389457908.39485797, '124.9090798',
                        '-0.126155', "-803485.9457897", "4564690846908.4059680458960", "485739857", "-4573875937",
                        None, "None", 'None']
    exception_text_values = [str(ShortHolder.MIN_VALUE - 1), str(ShortHolder.MAX_VALUE + 1), "value", 'string', 'a', "b",
                             '', "", True, False, "True", "False", 234.890, -7389457908.39485797, '124.9090798',
                             '-0.126155', "-803485.9457897", "4564690846908.4059680458960", "-4573875937", "8857349",
                             None, "None", 'None']
    valid_values = [ShortHolder.MIN_VALUE, ShortHolder.MAX_VALUE, 12345, ShortHolder.MIN_VALUE + 1,
                    ShortHolder.MAX_VALUE - 1]

    def test_init(self):
        short_holder = ShortHolder()
        assert short_holder.get() == 0

    def test_private_field(self):
        short_holder = ShortHolder()
        with pytest.raises(AttributeError):
            short_holder.value = 123

    def test_init_param(self):
        for tested_value in TestShortHolder.valid_values:
            short_holder = ShortHolder(tested_value)
            assert short_holder.get() == tested_value

    def test_init_exception(self):
        for tested_value in TestShortHolder.exception_values:
            with pytest.raises(Exception):
                short_holder = ShortHolder(tested_value)

    def test_to_string(self):
        for tested_value in TestShortHolder.valid_values:
            short_holder = ShortHolder(tested_value)
            assert short_holder.__str__().__eq__(str(tested_value))

    def test_equals(self):
        short_holder_1 = ShortHolder()
        short_holder_2 = ShortHolder()
        assert short_holder_1.__eq__(None) is False
        assert short_holder_1.__eq__(int("123")) is False
        assert short_holder_1.__eq__(short_holder_1) is True
        assert short_holder_1.__eq__(short_holder_2) is True
        short_holder_2.set(12345)
        assert short_holder_1.__eq__(short_holder_2) is False
