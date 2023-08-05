import pytest

from wsit.main.com.vsi.wsi.big_decimal import BigDecimal
from wsit.main.pyx.xml.rpc.holders.big_decimal_holder import BigDecimalHolder


class TestBigDecimalHolder:
    exception_values = ["value", 'string', 'a', "b", '', "", True, False, "True", "False", "0", "1", '0', '1', 234.890,
                        -7389457908.39485797, '124.9090798', '-0.126155', "-803485.9457897", "4564690846908.4059680450",
                        "485739857", "-4573875937", None, "None", 'None']

    exception_text_values = ["value", 'string', 'a', "b", '', "", True, False, "True", "False", None, "None", 'None',
                             234.890, -7389457908.39485797, -123456789.1234567890, -987654321, 123456789.1234567890,
                             0.299999999999999988897769753748434595763683319091796875]

    valid_values = ["0", "1", '0', '1', '124.9090798', '-0.126155', "-803485.94897",
                    "4564690846908.4059680458960", "485739857", "-4573875937", "123412345678901",
                    "9007199254740994000", "16777216", "-16777216", "-389475", "-1", "0.0", "0.0000123"]

    def test_init(self):
        big_decimal_holder = BigDecimalHolder()
        bd = BigDecimal.init_from_str("0.0")
        assert bd.__eq__(big_decimal_holder.get())

    def test_private_field(self):
        big_decimal_holder = BigDecimalHolder()
        with pytest.raises(AttributeError):
            big_decimal_holder.value = 123

    def test_init_param(self):
        for tested_value in TestBigDecimalHolder.valid_values:
            dec_value = BigDecimal.init_from_str(tested_value)
            big_decimal_holder = BigDecimalHolder(dec_value)
            assert dec_value.__eq__(big_decimal_holder.get())

    def test_to_string(self):
        for tested_value in TestBigDecimalHolder.valid_values:
            dec_value = BigDecimal.init_from_str(tested_value)
            big_decimal_holder = BigDecimalHolder(dec_value)
            assert dec_value.__str__().__eq__(big_decimal_holder.__str__())

    def test_equals(self):
        dec_value = BigDecimal.init_from_str("0.299999999999999988897769753748434595763683319091796875")
        big_decimal_holder_1 = BigDecimalHolder(dec_value)
        big_decimal_holder_2 = BigDecimalHolder(dec_value)
        big_decimal_holder_3 = BigDecimalHolder(BigDecimal(1000))
        assert big_decimal_holder_1.__eq__(None) is False
        assert big_decimal_holder_1.__eq__(int("123")) is False
        assert big_decimal_holder_1.__eq__(big_decimal_holder_1) is True
        assert big_decimal_holder_1.__eq__(big_decimal_holder_2) is True
        assert big_decimal_holder_1.__eq__(big_decimal_holder_3) is False
