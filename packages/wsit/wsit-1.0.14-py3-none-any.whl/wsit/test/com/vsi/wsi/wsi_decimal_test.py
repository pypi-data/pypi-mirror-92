import pytest

from wsit.main.com.vsi.wsi.big_decimal import BigDecimal
from wsit.main.com.vsi.wsi.wsi_decimal import WsiDecimal


class TestWsiDecimal:
    def test_init(self):
        wsi_decimal = WsiDecimal()
        zero_big_decimal = BigDecimal.init_from_str("0.0")
        assert wsi_decimal.get_value().__str__().__eq__(zero_big_decimal.__str__())
        assert wsi_decimal.get_value() == zero_big_decimal
        assert wsi_decimal.get_precision() == 0
        assert wsi_decimal.get_scale() == 0
        assert wsi_decimal.get_decimal_type() == 0

    def test_init_2(self):
        tested_value = "-123456789.123456789"
        wsi_decimal = WsiDecimal(tested_value)
        assert str(wsi_decimal).__eq__(tested_value)

    def test_init_3(self):
        tested_value = BigDecimal.init_from_str("2.7182818284590452353602874713527")
        wsi_decimal = WsiDecimal(tested_value)
        assert wsi_decimal.__str__().__eq__(tested_value.__str__())
        assert wsi_decimal.get_value() == tested_value

    def test_init_4(self):
        tested_value = BigDecimal.init_from_str("-2.7182818284590452353602874713527")
        scale = tested_value.get_scale()
        precision = 32
        dec_type = WsiDecimal.DTYPE_NL
        wsi_decimal = WsiDecimal.init_from_bd_value_precision_scale_dectype(tested_value, precision, scale, dec_type)
        assert wsi_decimal.__str__().__eq__(tested_value.__str__())
        assert wsi_decimal.get_value() == tested_value
        assert wsi_decimal.get_scale() == scale
        assert wsi_decimal.get_precision() == precision
        assert wsi_decimal.get_decimal_type() == dec_type

    def test_init_5(self):
        tested_value = BigDecimal.init_from_str("7182818284590452353602874713527.7182818284590452353602874713527")
        scale = tested_value.get_scale()
        precision = 62
        dec_type = WsiDecimal.DTYPE_NU
        wsi_decimal = WsiDecimal.init_from_bd_value_precision_scale_dectype(tested_value, precision, scale, dec_type)
        wsi_decimal_other = WsiDecimal(wsi_decimal)
        assert wsi_decimal.__str__().__eq__(wsi_decimal_other.__str__())
        assert wsi_decimal.get_value() == tested_value
        assert wsi_decimal.get_scale() == wsi_decimal_other.get_scale()
        assert wsi_decimal.get_precision() == wsi_decimal_other.get_precision()
        assert wsi_decimal.get_decimal_type() == wsi_decimal_other.get_decimal_type()

    def test_init_6(self):
        tested_value = BigDecimal(123)
        num123 = [48, 48, 48, 48, 48, 48, 48, 49, 50, 51]
        offset = 0
        precision = 10
        scale = tested_value.get_scale()
        dec_type = WsiDecimal.DTYPE_NU
        wsi_decimal = WsiDecimal.init_from_buffer_offset_precision_scale_dec_type(num123, offset, precision, scale, dec_type)
        assert wsi_decimal.get_scale() == scale
        assert wsi_decimal.get_precision() == precision
        assert wsi_decimal.get_decimal_type() == dec_type
        assert wsi_decimal.get_value() == tested_value
        assert wsi_decimal.__str__().__eq__(tested_value.__str__())

    def test_set_value_1(self):
        tested_value = BigDecimal.init_from_str("-32894709283740892734.28340892734098709861782364198764")
        wsi_decimal = WsiDecimal()
        wsi_decimal.set_value(tested_value)
        assert wsi_decimal.get_value() == tested_value
        assert wsi_decimal.__str__().__eq__(tested_value.__str__())

    def test_set_value_2(self):
        tested_value = "-32894709283740892734.28340892734098709861782364198764"
        wsi_decimal = WsiDecimal()
        wsi_decimal.set_value(tested_value)
        assert wsi_decimal.__str__().__eq__(tested_value)

    def test_set_value_3(self):
        tested_value = BigDecimal.init_from_str("-32894709283740892734.28340892734098709861782364198764")
        wsi_decimal = WsiDecimal(tested_value)
        wsi_decimal_other = WsiDecimal()
        wsi_decimal_other.set_value(wsi_decimal)
        assert wsi_decimal_other.get_value() == tested_value
        assert wsi_decimal_other.__str__().__eq__(tested_value.__str__())

    def test_set_value_4(self):
        wsi_decimal = WsiDecimal()
        tested_value = BigDecimal.init_from_str("123")
        wsi_decimal.set_scale(0)
        wsi_decimal.set_precision(3)
        num123 = [49, 50, 51]
        assert wsi_decimal.set_value_from_buffer_offset(num123, 0) == tested_value

    def test_set_value_5(self):
        wsi_decimal = WsiDecimal()
        tested_value = BigDecimal.init_from_str("123")
        num123 = [49, 50, 51]
        assert wsi_decimal.set_value_from_buffer_offset_precision_scale_dec_type(num123, 0, 3, 0, WsiDecimal.DTYPE_NU) == tested_value

    def test_set_precision(self):
        tested_value = 5
        wsi_decimal = WsiDecimal()
        wsi_decimal.set_precision(tested_value)
        assert wsi_decimal.get_precision() == tested_value

    def test_set_scale(self):
        tested_value = 10
        wsi_decimal = WsiDecimal()
        wsi_decimal.set_scale(tested_value)
        assert wsi_decimal.get_scale() == tested_value

    def test_set_decimal_type(self):
        tested_value = WsiDecimal.DTYPE_NL
        wsi_decimal = WsiDecimal()
        wsi_decimal.set_decimal_type(tested_value)
        assert wsi_decimal.get_decimal_type() == tested_value

    def test_set_attributes(self):
        precision = 200
        scale = 100
        dec_type = WsiDecimal.DTYPE_NRO
        wsi_decimal = WsiDecimal()
        wsi_decimal.set_attributes(precision, scale, dec_type)
        assert wsi_decimal.get_precision() == precision
        assert wsi_decimal.get_scale() == scale
        assert wsi_decimal.get_decimal_type() == dec_type

    def test_get_buffer_1(self):
        tested_value = "-123456.789"
        wsi_decimal = WsiDecimal(tested_value)
        wsi_decimal.set_scale(-3)
        wsi_decimal.set_precision(9)
        ret_array = wsi_decimal.get_buffer()
        str_from_bytes = "".join(map(chr, ret_array))
        assert str_from_bytes.__eq__("123456789")

    def test_get_buffer_2(self):
        tested_value = "-123456.789"
        wsi_decimal = WsiDecimal(tested_value)
        ret_array = wsi_decimal.get_buffer_from_precision_scale_dec_type(9, -2, WsiDecimal.DTYPE_NU)
        str_from_bytes = "".join(map(chr, ret_array))
        assert str_from_bytes.__eq__("012345678")

