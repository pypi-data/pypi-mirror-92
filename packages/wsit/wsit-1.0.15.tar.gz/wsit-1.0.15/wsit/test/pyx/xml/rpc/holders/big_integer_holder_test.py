import pytest

from wsit.main.pyx.xml.rpc.holders.big_integer_holder import BigIntegerHolder


class TestBigIntegerHolder:
    exception_values = ["value", 'string', 'a', "b", '', "", True, False, "True", "False", "0", "1", '0', '1', 234.890,
                        -7389457908.39485797, '124.9090798', '-0.126155', "-803485.9457897", "4564690846908.4059680450",
                        "485739857", "-4573875937", None, "None", 'None']

    exception_text_values = ["value", 'string', 'a', "b", '', "", True, False, "True", "False", None, "None", 'None',
                             234.890, -7389457908.39485797, -123456789.1234567890, 123456789.1234567890,
                             0.299999999999999988897769753748434595763683319091796875, '124.9090798', '-0.126155',
                             "-803485.9457897", "4564690846908.4059680450"]

    valid_values = [0, 1, -987654321, 598760760487603, 231029371908273012973892710387019287301982730182741908709760987,
                    -0, -1, -3409578397459384750394875938475039048750398475093847503984750398475096328767257648747607]

    def test_init(self):
        big_integer_holder = BigIntegerHolder()
        assert big_integer_holder.get() == 0

    def test_private_field(self):
        big_integer_holder = BigIntegerHolder()
        with pytest.raises(AttributeError):
            big_integer_holder.value = 123

    def test_init_param(self):
        for tested_value in TestBigIntegerHolder.valid_values:
            big_integer_holder = BigIntegerHolder(tested_value)
            assert tested_value == big_integer_holder.get()

    def test_init_param_exception(self):
        for tested_value in TestBigIntegerHolder.exception_values:
            with pytest.raises(Exception):
                big_integer_holder = BigIntegerHolder(tested_value)

    def test_to_string(self):
        for tested_value in TestBigIntegerHolder.valid_values:
            big_integer_holder = BigIntegerHolder(tested_value)
            assert str(tested_value).__eq__(big_integer_holder.__str__())

    def test_equals(self):
        tested_value = 99999999999999988897769753748434595763683319091796875
        big_integer_holder_1 = BigIntegerHolder(tested_value)
        big_integer_holder_2 = BigIntegerHolder(tested_value)
        big_integer_holder_3 = BigIntegerHolder(1000)
        assert big_integer_holder_1.__eq__(None) is False
        assert big_integer_holder_1.__eq__(int("123")) is False
        assert big_integer_holder_1.__eq__(big_integer_holder_1) is True
        assert big_integer_holder_1.__eq__(big_integer_holder_2) is True
        assert big_integer_holder_1.__eq__(big_integer_holder_3) is False
