import struct
import numpy
from wsit.main.pyx.xml.rpc.holders.byte_holder import ByteHolder
from wsit.main.pyx.xml.rpc.holders.int_holder import IntHolder
from wsit.main.pyx.xml.rpc.holders.long_holder import LongHolder
from wsit.main.pyx.xml.rpc.holders.short_holder import ShortHolder
from enum import Enum
from wsit.main.pyx.xml.rpc.holders.ubyte_holder import UByteHolder
from wsit.main.pyx.xml.rpc.holders.uint_holder import UIntHolder
from wsit.main.pyx.xml.rpc.holders.ulong_holder import ULongHolder
from wsit.main.pyx.xml.rpc.holders.ushort_holder import UShortHolder


class IntegerTypes(Enum):
    BYTE = 1
    SHORT = 2
    INT = 3
    LONG = 4
    UBYTE = 5
    USHORT = 6
    UINT = 7
    ULONG = 8
    EXT_BYTE = 9


class WsiUtils:
    min_max_values = {IntegerTypes.BYTE: (ByteHolder.MIN_VALUE, ByteHolder.MAX_VALUE),
                      IntegerTypes.SHORT: (ShortHolder.MIN_VALUE, ShortHolder.MAX_VALUE),
                      IntegerTypes.INT: (IntHolder.MIN_VALUE, IntHolder.MAX_VALUE),
                      IntegerTypes.LONG: (LongHolder.MIN_VALUE, LongHolder.MAX_VALUE),
                      IntegerTypes.UBYTE: (UByteHolder.MIN_VALUE, UByteHolder.MAX_VALUE),
                      IntegerTypes.USHORT: (UShortHolder.MIN_VALUE, UShortHolder.MAX_VALUE),
                      IntegerTypes.UINT: (UIntHolder.MIN_VALUE, UIntHolder.MAX_VALUE),
                      IntegerTypes.ULONG: (ULongHolder.MIN_VALUE, ULongHolder.MAX_VALUE),
                      IntegerTypes.EXT_BYTE: (ByteHolder.MIN_VALUE, UByteHolder.MAX_VALUE)}

    @staticmethod
    def check_type(input_value, correct_type):
        if type(input_value) is not correct_type:
            raise TypeError(
                "wrong type for " + str(input_value) + " argument: " + str(type(input_value)) + ", should be " + str(
                    correct_type))

    @staticmethod
    def is_list_type_of(input_list: list, input_type: type):
        WsiUtils.check_type(input_list, list)
        for el in input_list:
            if type(el) is not input_type:
                return False
        return True

    @staticmethod
    def check_list_type_of_intervals(input_list: list, input_type: IntegerTypes):
        WsiUtils.check_instance(input_list, list)
        for el in input_list:
            WsiUtils.check_value_interval(el, input_type)

    @staticmethod
    def check_list_type_of(input_list:list, input_type: type):
        WsiUtils.check_instance(input_list, list)
        for el in input_list:
            WsiUtils.check_instance(el, input_type)

    @staticmethod
    def check_instance(input_value, class_type):
        if not isinstance(input_value, class_type):
            raise TypeError(str(input_value) + " is not an instance of class " + str(class_type))

    @staticmethod
    def check_set_attr(obj_name, attr_name, value):
        if not hasattr(obj_name, attr_name):
            raise AttributeError('''Can't set attribute "{0}"'''.format(attr_name))
        object.__setattr__(obj_name, attr_name, value)

    @staticmethod
    def check_value_interval(value: int, int_type: 'IntegerTypes'):
        WsiUtils.check_type(value, int)
        WsiUtils.check_type(int_type, IntegerTypes)
        if value < WsiUtils.min_max_values.get(int_type)[0] or value > WsiUtils.min_max_values.get(int_type)[1]:
            raise ValueError("Value too small or too large for " + int_type.__str__() + ": " + value.__str__())

    @staticmethod
    def float_to_raw_int_bits(f):
        s = struct.pack('=f', f)
        return struct.unpack('=l', s)[0]

    @staticmethod
    def double_to_raw_int_bits(f):
        s = struct.pack('=d', f)
        return struct.unpack('=q', s)[0]

    @staticmethod
    def unsigned_right_shift(value, n):
        return (value % 0x100000000) >> n

    @staticmethod
    def int_to_float(i: int):
        WsiUtils.check_type(i, int)
        return numpy.float32(struct.unpack('!f', struct.pack('!i', i))[0])

    @staticmethod
    def int_to_double(i: int):
        WsiUtils.check_type(i, int)
        return struct.unpack('!d', struct.pack('!q', i))[0]

    @staticmethod
    def int_to_bytes(i: int):
        WsiUtils.check_type(i, int)
        if i == -1 or i == 0:
            return [numpy.int8(abs(i) * 255)]
        unpack_result = list(struct.unpack('BBBB', struct.pack('>i', i)))
        for i in range(len(unpack_result)):
            if unpack_result[i] not in [0, 255]:
                for j in range(i, len(unpack_result)):
                    unpack_result[j] = numpy.int8(unpack_result[j])
                return unpack_result[i:]

    @staticmethod
    def int_to_byte(i: int):
        WsiUtils.check_type(i, int)
        if i == -1 or i == 0:
            return [numpy.int8(abs(i) * 255)]
        unpack_result = list(struct.unpack('BBBB', struct.pack('>i', i)))
        for i in range(len(unpack_result)):
            if unpack_result[i] not in [0, 255]:
                return numpy.int8(unpack_result[i])

    @staticmethod
    def bytes_to_string(bytes: list) -> str:
        WsiUtils.check_list_type_of_intervals(bytes, IntegerTypes.BYTE)
        return "".join(map(chr, bytes))

    @staticmethod
    def array_deep(x):
        if x and isinstance(x, list):
            return 1 + max(WsiUtils.array_deep(i) for i in x)
        return 0

    @staticmethod
    def get_signed_int(int_value):
        if int_value & 0x80000000:
            int_value = -0x100000000 + int_value
        return int_value

    @staticmethod
    def get_unsigned_int(int_value):
        return int_value & 0xffffffff

    @staticmethod
    def get_unsigned_byte(int_value):
        return int_value & 0xff