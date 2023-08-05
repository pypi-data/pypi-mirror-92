import pytest

from wsit.main.pyx.xml.rpc.holders.char_holder import CharHolder


class TestCharHolder:
    exception_values = [-97038573098, 8470750398475, "value", 'string', '', "", True, False, "True", "False", 234.890,
                        -7389457908.39485797, '124.9090798', '-0.126155', "-803485.9457897", "4564690846908.4059045890",
                        "485739857", "-4573875937", None, "None", 'None', 0, 1]

    exception_text_values = [-97038573098, 8470750398475, '', "", True, False, 234.890, -7389457908.39485797, None]

    valid_text_values = ["value", 'string', "True", "False", '124.9090798', '-0.126155', "-803485.9457897",
                         "4564690846908.4059045890", "485739857", "-4573875937", "None", 'None']

    valid_values = ['\0', 'a', "b", "0", "1", '0', '1', '\t', '\n', '\r']

    def test_init(self):
        char_holder = CharHolder()
        assert char_holder.get() == '\0'

    def test_private_field(self):
        char_holder = CharHolder()
        with pytest.raises(AttributeError):
            char_holder.value = 123

    def test_init_param(self):
        for tested_value in TestCharHolder.valid_values:
            char_holder = CharHolder(tested_value)
            assert char_holder.get() == tested_value

    def test_init_exception(self):
        for tested_value in TestCharHolder.exception_values:
            with pytest.raises(Exception):
                char_holder = CharHolder(tested_value)

    def test_to_string(self):
        for tested_value in TestCharHolder.valid_values:
            char_holder = CharHolder(str(tested_value))
            assert str(tested_value).__eq__(char_holder.__str__())

    def test_equals(self):
        tested_value = '\n'
        char_holder_1 = CharHolder(tested_value)
        char_holder_2 = CharHolder(tested_value)
        char_holder_3 = CharHolder()
        assert char_holder_1.__eq__(None) is False
        assert char_holder_1.__eq__(int("123")) is False
        assert char_holder_1.__eq__(char_holder_1) is True
        assert char_holder_1.__eq__(char_holder_2) is True
        assert char_holder_1.__eq__(char_holder_3) is False
