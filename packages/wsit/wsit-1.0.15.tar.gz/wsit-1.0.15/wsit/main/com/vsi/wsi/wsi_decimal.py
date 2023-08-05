from typing import List

from wsit.main.com.vsi.wsi.big_decimal import BigDecimal
from wsit.main.com.vsi.wsi.wsi_utils import WsiUtils, IntegerTypes

"""
*  WsiDecimal
*     It provides a simple setter/getter class wrapping of BigDecimal (Decimal).
*     This will add the needed support for In/Out parameters into wrapped OpenVMS applications.
*
*     Internally, this class will be used to help marshall the
*     Decimals within structures and parameter lists.
"""


class WsiDecimal:
    DTYPE_NU = 15      # numeric string, unsigned
    DTYPE_NL = 16      # numeric string, left separate sign
    DTYPE_NLO = 17     # numeric string, left overpunched sign
    DTYPE_NR = 18      # numeric string, right separate sign
    DTYPE_NRO = 19     # numeric string, right overpunched sign
    DTYPE_NZ = 20      # numeric string, zoned sign
    DTYPE_P = 21       # packed decimal string

    def __init__(self, p_value=None):
        self.__value = None
        self.__precision = 0
        self.__scale = 0
        self.__decimal_type = 0

        if p_value is None:
            self.__value = BigDecimal.init_from_str("0.0")
        elif type(p_value) is str:
            self.__value = BigDecimal.init_from_str(p_value)
        elif type(p_value) is BigDecimal:
            self.__value = p_value
            self.__scale = p_value.get_scale()
        elif isinstance(p_value, WsiDecimal):
            self.__value = p_value.get_value()
            self.__precision = p_value.get_precision()
            self.__scale = p_value.get_scale()
            self.__decimal_type = p_value.get_decimal_type()
        else:
            raise TypeError("wrong argument type: " + type(p_value))

    @classmethod
    def init_from_bd_value_precision_scale_dectype(cls, bd_value: BigDecimal, precision: int, scale: int, dec_type: int) -> 'WsiDecimal':
        WsiUtils.check_instance(bd_value, BigDecimal)
        WsiUtils.check_type(precision, int)
        WsiUtils.check_type(scale, int)
        WsiUtils.check_type(dec_type, int)
        wsi_decimal = cls()
        wsi_decimal.__value = bd_value
        wsi_decimal.__precision = precision
        wsi_decimal.__scale = scale
        wsi_decimal.__decimal_type = dec_type
        return wsi_decimal

    # Constructs this class from a Byte Array
    @classmethod
    def init_from_buffer_offset_precision_scale_dec_type(cls, buffer: List[int], offset: int, precision: int, scale: int, dec_type: int)->'WsiDecimal':
        wsi_decimal = cls()
        wsi_decimal.set_value_from_buffer_offset_precision_scale_dec_type(buffer, offset, precision, scale, dec_type)
        return wsi_decimal

    def get_value(self) -> BigDecimal:
        return self.__value

    def set_value(self, p_value):
        if type(p_value) is BigDecimal:
            self.__value = p_value
        elif type(p_value) is str:
            self.__value = BigDecimal.init_from_str(p_value)
        elif isinstance(p_value, WsiDecimal):
            self.__precision = p_value.get_precision()
            self.__scale = p_value.get_scale()
            self.__decimal_type = p_value.get_decimal_type()
            self.__value = p_value.get_value()

    def get_precision(self) -> int:
        return self.__precision

    def set_precision(self, new_precision: int):
        WsiUtils.check_type(new_precision, int)
        self.__precision = new_precision

    def get_scale(self) -> int:
        return self.__scale

    def set_scale(self, new_scale: int):
        WsiUtils.check_type(new_scale, int)
        self.__scale = new_scale

    # Returns the internal OpenVMS Decimal Datatype value.
    def get_decimal_type(self) -> int:
        return self.__decimal_type

    # Sets the internal OpenVMS Decimal Datatype value.
    def set_decimal_type(self, new_decimal_type: int):
        WsiUtils.check_type(new_decimal_type, int)
        self.__decimal_type = new_decimal_type

    def set_attributes(self, precision: int, scale: int, dec_type: int):
        WsiUtils.check_type(precision, int)
        WsiUtils.check_type(scale, int)
        WsiUtils.check_type(dec_type, int)
        self.__precision = precision
        self.__scale = scale
        self.__decimal_type = dec_type

    def get_buffer(self) -> List[int]:
        array_size = self.get_byte_count(self.__precision, self.__decimal_type)
        ret_array = [0]*array_size
        self.get_buffer_s(ret_array, 0, self.__value, self.__precision, self.__scale, self.__decimal_type)
        return ret_array

    def get_buffer_from_precision_scale_dec_type(self, precision: int, scale: int, dec_type: int):
        WsiUtils.check_type(precision, int)
        WsiUtils.check_type(scale, int)
        WsiUtils.check_type(dec_type, int)
        self.__precision = precision
        self.__scale = scale
        self.__decimal_type = dec_type
        array_size = self.get_byte_count(self.__precision, self.__decimal_type)
        ret_array = [0]*array_size
        WsiDecimal.get_buffer_s(ret_array, 0, self.__value, self.__precision, self.__scale, self.__decimal_type)
        return ret_array

    def get_buffer_from_buffer_offset_precision_scale_dec_type(self, buffer: List[int], offset: int, precision: int,
                                                               scale: int, dec_type: int) -> List[int]:
        WsiUtils.check_type(precision, int)
        WsiUtils.check_type(scale, int)
        WsiUtils.check_type(dec_type, int)
        self.__precision = precision
        self.__scale = scale
        self.__decimal_type = dec_type
        return self.get_buffer_s(buffer, offset, self.__value, self.__precision, self.__scale, self.__decimal_type)

    def set_value_from_buffer_offset(self, buffer: List[int], offset: int) -> BigDecimal:
        self.__value = self.set_value_s(buffer, offset, self.__precision, self.__scale, self.__decimal_type)
        return self.__value

    def set_value_from_buffer_offset_precision_scale_dec_type(self, buffer: List[int], offset: int,
                                                              precision: int, scale: int, dec_type: int) -> BigDecimal:
        WsiUtils.check_type(precision, int)
        WsiUtils.check_type(scale, int)
        WsiUtils.check_type(dec_type, int)
        self.__precision = precision
        self.__scale = scale
        self.__decimal_type = dec_type
        self.__value = self.set_value_s(buffer, offset, self.__precision, self.__scale, self.__decimal_type)
        return self.__value

    """
    Static Encode method
     It builds the appropriate byte layout, based on its OpenVMS
     datatype, into the provided byte array and offset.
     returns ret_array
    """
    @staticmethod
    def get_buffer_s(ret_array: List[int], p_offset: int, value: BigDecimal, precision: int,
                     scale: int, dec_type: int):
        WsiUtils.check_list_type_of_intervals(ret_array, IntegerTypes.BYTE)
        WsiUtils.check_type(p_offset, int)
        WsiUtils.check_type(value, BigDecimal)
        WsiUtils.check_type(precision, int)
        WsiUtils.check_type(scale, int)
        WsiUtils.check_type(dec_type, int)
        # Handle Packed Decimal numbers separately
        if dec_type == WsiDecimal.DTYPE_P:
            return WsiDecimal.get_buffer_s_packed(ret_array, p_offset, value, precision, scale, dec_type)

        curr_offset = p_offset
        fix_up_position = 0
        sign_flag = value.sign()

        # least significant digits will be truncated quietly
        str_value = value.move_point_left(scale).get_whole_part().__str__()
        work_array = str_value.encode()
        w_offset = 0
        if work_array[0] == b'-'[0] or work_array[0] == b'+'[0]:
            w_offset += 1

        # Throw an Exception if remaining decimal is too big
        value_length = len(work_array) - w_offset
        if value_length > precision:
            raise ValueError("Number is too large, can't be passed without losing significant digits.")

        if dec_type == WsiDecimal.DTYPE_NL:
            if sign_flag == -1:
                ret_array[curr_offset] = 45
            else:
                ret_array[curr_offset] = 32
            curr_offset += 1

        if dec_type == WsiDecimal.DTYPE_NLO:
            fix_up_position = curr_offset

        # Put in zero padding as needed
        for i in range(precision - value_length):
            ret_array[curr_offset] = 48
            curr_offset += 1

        for i in range(value_length):
            ret_array[curr_offset] = work_array[w_offset]
            curr_offset += 1
            w_offset += 1

        if dec_type == WsiDecimal.DTYPE_NRO or dec_type == WsiDecimal.DTYPE_NZ:
            fix_up_position = curr_offset - 1

        if dec_type == WsiDecimal.DTYPE_NR:
            if sign_flag == -1:
                ret_array[curr_offset] = 45
            ret_array[curr_offset] = 32
            curr_offset += 1

        # Fixup the sign for Zoned & Overpunch Decimals
        if dec_type == WsiDecimal.DTYPE_NLO or dec_type == WsiDecimal.DTYPE_NRO:
            if sign_flag == -1:
                if ret_array[fix_up_position] == 48:
                    ret_array[fix_up_position] = 125
                else:
                    ret_array[fix_up_position] = ret_array[fix_up_position] + 25
            else:
                if ret_array[fix_up_position] == 48:
                    ret_array[fix_up_position] = 123
                else:
                    ret_array[fix_up_position] = ret_array[fix_up_position] + 16
        elif dec_type == WsiDecimal.DTYPE_NZ:
            if sign_flag == -1:
                ret_array[fix_up_position] = ret_array[fix_up_position] + 64
        return ret_array

    # Private Encode method to handle Packed Decimals
    # returns ret_array = List[int]
    @staticmethod
    def get_buffer_s_packed(ret_array: List[int], p_offset: int, value: BigDecimal, precision: int, scale: int, dec_type: int) -> List[int]:
        WsiUtils.check_list_type_of_intervals(ret_array, IntegerTypes.BYTE)
        WsiUtils.check_type(p_offset, int)
        WsiUtils.check_type(value, BigDecimal)
        WsiUtils.check_type(precision, int)
        WsiUtils.check_type(scale, int)
        WsiUtils.check_type(dec_type, int)

        curr_offset = p_offset
        nibble_offset = 0
        sign_flag = value.sign()

        # least significant digits will be truncated quietly
        str_value = ((value.move_point_left(scale)).get_whole_part()).__str__()
        work_array = [0]*len(str_value)
        for i in range(len(str_value)):
            work_array[i] = ord(str_value[i])
        w_offset = 0
        if work_array[0] == 45 or work_array[0] == 43:
            w_offset += 1

        # Throw an Exception if remaining decimal is too big
        value_length = len(work_array) - w_offset
        if value_length > precision:
            raise ValueError("Number is too large, can't be passed without losing significant digits.")

        # If precision > actual value, put in zero padding at front
        for i in range(precision - value_length):
            if nibble_offset & 1 == 0:
                nibble_offset += 1
                ret_array[curr_offset] = 0
            else:
                nibble_offset += 1
                curr_offset += 1

        # Even length precisions need 1 more zero nibble
        if precision & 1 == 0:
            if nibble_offset & 1 == 0:
                nibble_offset += 1
                ret_array[curr_offset] = 0
            else:
                curr_offset += 1

        # Move the values into Packed format
        for i in range(value_length):
            if nibble_offset & 1 == 0:
                nibble_offset += 1
                ret_array[curr_offset] = (work_array[w_offset] - 48) << 4
                w_offset += 1
            else:
                nibble_offset += 1
                ret_array[curr_offset] += (work_array[w_offset] - 48)
                curr_offset += 1
                w_offset += 1

        # Add the sign nibble
        if sign_flag == -1:
            ret_array[curr_offset] += 13
        else:
            ret_array[curr_offset] += 12
        return ret_array

    """
    Static Decode method
     It creates a BigDecimal object from a value found at a given
     buffer & offset. The value within the buffer is decoded based
     on the OpenVMS datatype.
     Returns BigDecimal
     """
    @staticmethod
    def set_value_s(buffer: List[int], offset: int, precision: int, scale: int, dec_type: int) -> BigDecimal:
        WsiUtils.check_list_type_of_intervals(buffer, IntegerTypes.EXT_BYTE)
        WsiUtils.check_type(offset, int)
        WsiUtils.check_type(precision, int)
        WsiUtils.check_type(scale, int)
        WsiUtils.check_type(dec_type, int)

        # Handle Packed Decimal numbers seperately
        if dec_type == WsiDecimal.DTYPE_P:
            return WsiDecimal.set_value_s_packed(buffer, offset, precision, scale, dec_type)

        work_offset = 0
        work_array = [0]*(precision+2)
        byte_cnt = WsiDecimal.get_byte_count(precision, dec_type)
        lb_offset = byte_cnt + offset - 1

        # Add a negative sign if needed, decode in process
        sign_flag = 1
        sign_offset = offset
        if dec_type == WsiDecimal.DTYPE_NL:
            if buffer[offset] == 45:
                offset += 1
                sign_flag = -1
            byte_cnt -= 1
        elif dec_type == WsiDecimal.DTYPE_NR:
            if buffer[lb_offset] == 45:
                lb_offset -= 1
                sign_flag = -1
            byte_cnt -= 1
        elif dec_type == WsiDecimal.DTYPE_NLO or dec_type == WsiDecimal.DTYPE_NRO:
            if dec_type == WsiDecimal.DTYPE_NRO:
                sign_offset = lb_offset
            if buffer[sign_offset] == 125 or (73 < buffer[sign_offset] < 83):
                sign_flag = -1
                if buffer[sign_offset] == 125:
                    buffer[sign_offset] = 48
                else:
                    buffer[sign_offset] = buffer[sign_offset] - 25
            else:
                if buffer[sign_offset] == 123:
                    buffer[sign_offset] = 48
                else:
                    buffer[sign_offset] = buffer[sign_offset] - 16
        elif dec_type == WsiDecimal.DTYPE_NZ:
            if buffer[lb_offset] > 57:
                sign_flag = -1
                buffer[lb_offset] = buffer[lb_offset] - 64
        if sign_flag == -1:
            work_array[work_offset] = '-'
            work_offset += 1

        # loop through numbers
        while offset <= lb_offset:
            work_array[work_offset] = buffer[offset]
            work_offset += 1
            offset += 1

        # Create BigDecimal from created array
        str_from_bytes = "".join(map(chr, work_array[:work_offset]))
        ret_decimal = BigDecimal.init_from_str(str_from_bytes)

        # Shift to proper scale
        ret_decimal = ret_decimal.move_point_right(scale)
        return ret_decimal

    """
    Static Decode method to decode Packed numerics
    It creates a BigDecimal object from a value found at a given
    buffer & offset. The value within the buffer is decoded as a Packed.
    Returns BigDecimal
    """
    @staticmethod
    def set_value_s_packed(buffer: List[int], offset: int, precision: int, scale: int, dec_type: int):
        WsiUtils.check_list_type_of_intervals(buffer, IntegerTypes.BYTE)
        WsiUtils.check_type(offset, int)
        WsiUtils.check_type(precision, int)
        WsiUtils.check_type(scale, int)
        WsiUtils.check_type(dec_type, int)

        work_offset = 0
        work_array = [0]*(precision+2)
        byte_cnt = WsiDecimal.get_byte_count(precision, dec_type)
        lb_offset = byte_cnt + offset - 1

        # Add a negative sign if needed
        if buffer[lb_offset] & 1 == 1 and buffer[lb_offset] & 15 != 15:
            work_array[work_offset] = '-'
            work_offset += 1

        # Skip first 0 if precision is even
        nibble_offset = 0
        if precision & 1 == 0:
            nibble_offset += 1

        # loop through numbers
        for i in range(nibble_offset, precision + nibble_offset):
            if (i & 1) == 0:
                work_array[work_offset] = ((WsiUtils.unsigned_right_shift(buffer[offset], 4)) & 0xF) + 48
            else:
                work_array[work_offset] = (buffer[offset] & 0xF) + 48
                offset += 1
            work_offset += 1

        # Create BigDecimal from created array
        str_from_bytes = "".join(map(chr, work_array[:work_offset]))
        ret_decimal = BigDecimal.init_from_str(str_from_bytes)

        # Shift to proper scale
        ret_decimal = ret_decimal.move_point_right(scale)

        return ret_decimal

    """
    Static method to return actual bytes used based on Decimal Datatype
    """
    @staticmethod
    def get_byte_count(precision: int, dec_type: int) -> int:
        WsiUtils.check_type(precision, int)
        WsiUtils.check_type(dec_type, int)
        if dec_type == WsiDecimal.DTYPE_NL or dec_type == WsiDecimal.DTYPE_NR:
            precision += 1
        elif dec_type == WsiDecimal.DTYPE_P:
            precision = int(precision/2) + 1
        return precision

    def __str__(self) -> str:
        return str(self.__value)

