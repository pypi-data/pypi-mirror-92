import pytest

from wsit.main.pyx.xml.rpc.holders.boolean_holder import BooleanHolder


class TestBooleanHolder:
    exception_values = ["value", 'string', 'a', "b", '', "", "True", "False", "true", "false", "0", "1", '0', '1', 0, 1,
                        42874029808374, -84563865890, 928374.09748724, -0.000046537658736, '124.9090798', '-0.126155',
                        "-803485.9457897", "4564690846908.4059680458960", "485739857", "-4573875937", None, "None",
                        'None']
    exception_text_values = ["value", 'string', 'a', "b", '', "", -84563858, 88979, 928374.09748724, -0.000046537658736,
                             '124.9090798', '-0.126155', "-803485.9457897", "4564690846908.40596458960", "485739857987",
                             "-4573875937", None, "None", 'None', "0", "1", '0', '1', 0, 1, True, False]
    valid_values = [True, False]
    valid_text_values = ["True", "False", 'True', 'False', "true", "false", 'true', 'false']

    def test_init(self):
        boolean_holder = BooleanHolder()
        assert boolean_holder.get() is False

    def test_private_field(self):
        boolean_holder = BooleanHolder()
        with pytest.raises(AttributeError):
            boolean_holder.value = 123

    def test_init_param(self):
        for tested_value in TestBooleanHolder.valid_values:
            boolean_holder = BooleanHolder(tested_value)
            assert boolean_holder.get() is tested_value

    def test_init_exception(self):
        for tested_value in TestBooleanHolder.exception_values:
            with pytest.raises(Exception):
                boolean_holder = BooleanHolder(tested_value)

    def test_to_string(self):
        for tested_value in TestBooleanHolder.valid_values:
            boolean_holder = BooleanHolder(tested_value)
            assert boolean_holder.__str__().__eq__(str(tested_value))

    def test_equals(self):
        boolean_holder_1 = BooleanHolder()
        boolean_holder_2 = BooleanHolder()
        assert boolean_holder_1.__eq__(None) is False
        assert boolean_holder_1.__eq__(int("123")) is False
        assert boolean_holder_1.__eq__(boolean_holder_1) is True
        assert boolean_holder_1.__eq__(boolean_holder_2) is True
        boolean_holder_2.set(True)
        assert boolean_holder_1.__eq__(boolean_holder_2) is False
