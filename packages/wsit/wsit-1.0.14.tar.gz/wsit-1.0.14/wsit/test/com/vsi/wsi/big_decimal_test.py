import pytest

from wsit.main.com.vsi.wsi.big_decimal import BigDecimal


class TestBigDecimal:
    valid_values_zero_scale = [9007199254740994000, 16777216, -16777216, 0, 1, -389475, -0, -1, 5678]
    valid_values_with_scale = [(9007199254740994000, 6, "9007199254740.994000"), (123, 7, "0.0000123"),
                               (0, 2, "0.00"), (12, 0, "12"), (-10050000000, 5, "-100500.00000"), (11, 0, "11")]
    exception_values_with_scale = [(9007199254740994000, -6, "9007199254740994000000000"), (123, -5, "12300000")]
    exception_values_zero_scale = [9007199254.740994000, 1677.7216, -16.777216, 0.0, 0.1, -0.00389475, -0.0, -1.0,
                                   True, False, "True", "False", None, "None"]
    valid_str_values = ["9007199254740994000", "16777216", "-16777216", "0", "1", "-389475", "-1", "0.0", "0.0000123"]

    def test_init(self):
        for int_value in TestBigDecimal.valid_values_zero_scale:
            big_decimal = BigDecimal(int_value)
            assert big_decimal.get_scale() == 0
            assert str(big_decimal).__eq__(str(int_value))

    def test_init_exception(self):
        for exception_value in TestBigDecimal.exception_values_zero_scale + TestBigDecimal.valid_str_values:
            with pytest.raises(Exception):
                big_decimal = BigDecimal(exception_value)

    def test_init_with_scale(self):
        for tested_set in TestBigDecimal.valid_values_with_scale:
            big_decimal = BigDecimal(tested_set[0], tested_set[1])
            assert str(big_decimal).__eq__(tested_set[2])

    def test_init_from_str(self):
        for str_value in TestBigDecimal.valid_str_values:
            big_decimal = BigDecimal.init_from_str(str_value)
            assert str(big_decimal).__eq__(str_value)

    def test_private_field(self):
        big_decimal = BigDecimal(12)
        with pytest.raises(AttributeError):
            big_decimal.value = 123
