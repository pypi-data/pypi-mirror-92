import re

from wsit.main.com.vsi.wsi.wsi_utils import WsiUtils
from wsit.main.pyx.xml.rpc.holders.int_holder import IntHolder


class BigDecimal:
    __big_int_value = 0
    __decimal_count = 0
    decimal_separator = '.'

    def __init__(self, int_value: int, decimals: int = 0):
        WsiUtils.check_type(int_value, int)
        WsiUtils.check_type(decimals, int)
        self.__big_int_value = int_value
        self.__decimal_count = decimals

    @classmethod
    def init_from_str(cls, str_value: str) -> 'BigDecimal':
        WsiUtils.check_type(str_value, str)
        pattern_with_point = '^-?\\d+' + BigDecimal.decimal_separator + '\\d+$'
        pattern_no_point = '^-?\\d+'
        decimals = 0
        if re.match(pattern_with_point, str_value) or re.match(pattern_no_point, str_value):
            if str_value.find(BigDecimal.decimal_separator) >= 0:
                decimals = len(str_value) - str_value.find(BigDecimal.decimal_separator) - 1
                str_value = str_value.replace(BigDecimal.decimal_separator, "")
            int_value = int(str_value)
            return cls(int_value, decimals)
        else:
            raise ValueError("value must be a string representation of an int or float types")

    def get_scale(self) -> int:
        return self.__decimal_count

    def get_precision(self) -> int:
        str_value = self.__str__()
        precision = len(str_value)
        if str_value.find(".") >= 0:
            precision -= 1
        if str_value.find("-") >= 0:
            precision -= 1
        return precision

    def sign(self) -> int:
        if self.__big_int_value >= 0:
            return 1
        return -1

    def move_point_left(self, n: int) -> 'BigDecimal':
        WsiUtils.check_type(n, int)
        # Cannot use movePointRight(-n) in case of n==Integer.MIN_VALUE
        new_scale = self.check_scale(self.__decimal_count + n)
        num = BigDecimal(self.__big_int_value, new_scale)
        if num.get_scale() < 0:
            return BigDecimal(num.__big_int_value * pow(10, abs(num.get_scale())))
        return num

    def move_point_right(self, n: int) -> 'BigDecimal':
        # Cannot use movePointLeft(-n) in case of n==Integer.MIN_VALUE
        new_scale = self.check_scale(self.__decimal_count - n)
        num = BigDecimal(self.__big_int_value, new_scale)
        if num.get_scale() < 0:
            return BigDecimal(num.__big_int_value * pow(10, abs(num.get_scale())))
        return num

    def check_scale(self, val: int) -> int:
        if val > IntHolder.MAX_VALUE:
            val = IntHolder.MAX_VALUE
        elif val < IntHolder.MIN_VALUE:
            val = IntHolder.MIN_VALUE
        return val

    def get_whole_part(self) -> int:
        return int(self.__big_int_value / pow(10, self.__decimal_count))

    def __str__(self) -> str:
        str_value = str(abs(self.__big_int_value))
        if self.__decimal_count > 0:
            str_value = str_value.rjust(self.__decimal_count + 1, '0')
            point_index = len(str_value) - self.__decimal_count
            str_value = str_value[:point_index] + self.decimal_separator + str_value[point_index:]
        if self.sign() < 0:
            str_value = '-' + str_value
        return str_value

    def __setattr__(self, name, value):
        WsiUtils.check_set_attr(self, name, value)

    def __eq__(self, obj):
        if isinstance(obj, BigDecimal):
            if self.__decimal_count != obj.__decimal_count:
                return False
            elif self.__big_int_value == obj.__big_int_value:
                return True
        return False
