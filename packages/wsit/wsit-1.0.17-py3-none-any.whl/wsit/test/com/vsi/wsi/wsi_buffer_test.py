import datetime

import numpy
import pytest
from numpy import float32

from wsit.main.com.vsi.wsi.big_decimal import BigDecimal
from wsit.main.com.vsi.wsi.wsi_array import WsiArray
from wsit.main.com.vsi.wsi.wsi_buffer import WsiBuffer
from wsit.main.com.vsi.wsi.wsi_decimal import WsiDecimal
from wsit.main.com.vsi.wsi.wsi_structure import WsiStructure


class TestWsiBuffer:
    def test_init(self):
        wsi_buffer = WsiBuffer()
        """The following constants are used to identify specific OpenVMS datatypes."""
        """Atomic data types:"""
        assert wsi_buffer.DTYPE_Z == 0  # unspecified
        assert wsi_buffer.DTYPE_BU == 2  # byte (unsigned);  8-bit unsigned quantity
        assert wsi_buffer.DTYPE_WU == 3  # word (unsigned);  16-bit unsigned quantity
        assert wsi_buffer.DTYPE_LU == 4  # longword (unsigned);  32-bit unsigned quantity
        assert wsi_buffer.DTYPE_QU == 5  # quadword (unsigned);  64-bit unsigned quantity
        assert wsi_buffer.DTYPE_OU == 25  # octaword (unsigned);  128-bit unsigned quantity
        assert wsi_buffer.DTYPE_B == 6  # byte integer (signed);  8-bit signed 2's-complement integer
        assert wsi_buffer.DTYPE_W == 7  # word integer (signed);  16-bit signed 2's-complement integer
        assert wsi_buffer.DTYPE_L == 8  # longword integer (signed);  32-bit signed 2's-complement integer
        assert wsi_buffer.DTYPE_Q == 9  # quadword integer (signed);  64-bit signed 2's-complement integer
        assert wsi_buffer.DTYPE_O == 26  # octaword integer (signed);  128-bit signed 2's-complement integer
        assert wsi_buffer.DTYPE_F == 10  # F_floating;  32-bit single-precision floating point
        assert wsi_buffer.DTYPE_D == 11  # D_floating;  64-bit double-precision floating point
        assert wsi_buffer.DTYPE_G == 27  # G_floating;  64-bit double-precision floating point
        assert wsi_buffer.DTYPE_H == 28  # H_floating;  128-bit quadruple-precision floating point
        assert wsi_buffer.DTYPE_FC == 12  # F_floating complex
        assert wsi_buffer.DTYPE_DC == 13  # D_floating complex
        assert wsi_buffer.DTYPE_GC == 29  # G_floating complex
        assert wsi_buffer.DTYPE_HC == 30  # H_floating complex
        assert wsi_buffer.DTYPE_CIT == 31  # COBOL Intermediate Temporary

        """String data types:"""
        assert wsi_buffer.DTYPE_T == 14  # character string;  a single 8-bit character or a sequence of characters
        assert wsi_buffer.DTYPE_VT == 37  # varying character string;  16-bit count, followed by a string
        assert wsi_buffer.DTYPE_NU == 15  # numeric string, unsigned
        assert wsi_buffer.DTYPE_NL == 16  # numeric string, left separate sign
        assert wsi_buffer.DTYPE_NLO == 17  # numeric string, left overpunched sign
        assert wsi_buffer.DTYPE_NR == 18  # numeric string, right separate sign
        assert wsi_buffer.DTYPE_NRO == 19  # numeric string, right overpunched sign
        assert wsi_buffer.DTYPE_NZ == 20  # numeric string, zoned sign
        assert wsi_buffer.DTYPE_P == 21  # packed decimal string
        assert wsi_buffer.DTYPE_V == 1  # aligned bit string
        assert wsi_buffer.DTYPE_VU == 34  # unaligned bit string

        """IEEE data types:"""
        assert wsi_buffer.DTYPE_FS == 52  # IEEE float basic single S
        assert wsi_buffer.DTYPE_FT == 53  # IEEE float basic double T
        assert wsi_buffer.DTYPE_FSC == 54  # IEEE float basic single S complex
        assert wsi_buffer.DTYPE_FTC == 55  # IEEE float basic double T complex
        assert wsi_buffer.DTYPE_FX == 57  # IEEE float basic extended
        assert wsi_buffer.DTYPE_FXC == 58  # IEEE float complex extended

        """Miscellaneous data types:"""
        assert wsi_buffer.DTYPE_ZI == 22  # sequence of instructions
        assert wsi_buffer.DTYPE_ZEM == 23  # procedure entry mask
        assert wsi_buffer.DTYPE_DSC == 24  # descriptor
        assert wsi_buffer.DTYPE_BPV == 32  # bound procedure value
        assert wsi_buffer.DTYPE_BLV == 33  # bound label value
        assert wsi_buffer.DTYPE_ADT == 35  # absolute date and time

        """BridgeWorks specific data types:"""
        assert wsi_buffer.DTYPE_STRUCT == 77  # BWX Structure

        """Constants for the various class types encountered"""
        assert wsi_buffer.CLASS_S == 1  # Static/Scalar
        assert wsi_buffer.CLASS_D == 2  # Dynamic String
        assert wsi_buffer.CLASS_A == 4  # Array
        assert wsi_buffer.CLASS_SD == 9  # Scaled Decimal
        assert wsi_buffer.CLASS_NCA == 10  # Non-Contiguous Array
        assert wsi_buffer.CLASS_VS == 11  # Variant String
        assert wsi_buffer.CLASS_VSA == 12  # Variant String Array

    def test_init_by_buf_size(self):
        buf_size = 10
        m_buffer_test = [0] * buf_size
        wsi_buffer = WsiBuffer.init_by_buf_size(buf_size)
        assert wsi_buffer.get_buf_size() == buf_size
        assert wsi_buffer.get_buffer_internal() == m_buffer_test

    def test_init_by_buffer(self):
        m_buffer_test = [1, 2, 3]
        wsi_buffer = WsiBuffer.init_by_buffer(m_buffer_test)
        assert wsi_buffer.get_buffer_internal() == m_buffer_test

    def test_init_by_buffer_buf_base(self):
        m_buffer_test = [1, 2, 3]
        buf_base = 3
        wsi_buffer = WsiBuffer.init_by_buffer_buf_base(m_buffer_test, buf_base)
        assert wsi_buffer.get_buffer_internal() == m_buffer_test
        assert wsi_buffer.get_buf_size() == len(m_buffer_test)
        assert wsi_buffer.get_base() == buf_base

        m_buffer_test = []
        buf_base = 0
        wsi_buffer = WsiBuffer.init_by_buffer_buf_base(m_buffer_test, buf_base)
        assert wsi_buffer.get_buffer_internal() == []
        assert wsi_buffer.get_buf_size() == buf_base
        assert wsi_buffer.get_base() == buf_base

    def test_init_by_buffer_buf_base_exception(self):
        m_buffer_test = [1, 2, 3]
        buf_base = 4
        with pytest.raises(Exception):
            wsi_buffer = WsiBuffer.init_by_buffer_buf_base(m_buffer_test, buf_base)

    def test_init_by_wsi_buffer(self):
        m_buffer_test = [1, 2, 3]
        wsi_buffer = WsiBuffer.init_by_buffer(m_buffer_test)
        wsi_buffer_other = WsiBuffer.init_by_wsi_buffer(wsi_buffer)
        assert wsi_buffer_other.get_buffer_internal() == m_buffer_test
        assert wsi_buffer_other.get_buf_size() == len(m_buffer_test)
        assert wsi_buffer_other.get_base() == 0

        m_buffer_test = []
        wsi_buffer = WsiBuffer.init_by_buffer(m_buffer_test)
        wsi_buffer_other = WsiBuffer.init_by_wsi_buffer(wsi_buffer)
        assert wsi_buffer_other.get_buffer_internal() == []
        assert wsi_buffer_other.get_buf_size() == 0
        assert wsi_buffer_other.get_base() == 0

    def test_init_by_wsi_buffer_buf_base(self):
        m_buffer_test = [1, 2, 3]
        buf_base = len(m_buffer_test)
        wsi_buffer = WsiBuffer.init_by_buffer(m_buffer_test)
        wsi_buffer_other = WsiBuffer.init_by_wsi_buffer_buf_base(wsi_buffer, buf_base)
        assert wsi_buffer_other.get_buffer_internal() == m_buffer_test
        assert wsi_buffer_other.get_buf_size() == len(m_buffer_test)

    def test_init_by_wsi_buffer_buf_base_exception(self):
        m_buffer_test = [1, 2, 3]
        buf_base = 5
        wsi_buffer = WsiBuffer.init_by_buffer(m_buffer_test)
        with pytest.raises(Exception):
            wsi_buffer_other = WsiBuffer.init_by_wsi_buffer_buf_base(wsi_buffer, buf_base)

    def test_init_by_wsi_buffer_start_pos_len(self):
        m_buffer_test = [1, 2, 3]
        start_pos_test = 0
        len_test = 0
        wsi_buffer = WsiBuffer.init_by_buffer(m_buffer_test)
        wsi_buffer_other = WsiBuffer.init_by_wsi_buffer_start_pos_len(wsi_buffer, start_pos_test, len_test)
        assert len(wsi_buffer_other.get_buffer()) == 0
        assert wsi_buffer_other.get_buffer() is not None

        start_pos_test = 4
        wsi_buffer_other = WsiBuffer.init_by_wsi_buffer_start_pos_len(wsi_buffer, start_pos_test, len_test)
        assert wsi_buffer_other.get_buffer_internal() == []

        start_pos_test = 2
        wsi_buffer_other = WsiBuffer.init_by_wsi_buffer_start_pos_len(wsi_buffer, start_pos_test, len_test)
        assert len(wsi_buffer_other.get_buffer()) == 0
        assert wsi_buffer_other.get_buffer() is not None

    def test_align_to(self):
        m_buffer_test = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
        wsi_buffer = WsiBuffer.init_by_buffer(m_buffer_test)

        int_value = 0
        wsi_buffer.align_to(int_value)
        assert wsi_buffer.m_cur_pos == int_value

        # newSize = mAllocSize + mReallocSize
        int_value = 7
        wsi_buffer.m_cur_pos = int_value
        m_alloc_size_test = wsi_buffer.get_realloc_size() + wsi_buffer.get_buf_size()
        tested_array = [0] * m_alloc_size_test
        tested_array = m_buffer_test[:int_value] + tested_array[int_value:]
        wsi_buffer.align_to(int_value)
        assert wsi_buffer.get_buffer_internal() == tested_array
        assert wsi_buffer.get_buf_size() == m_alloc_size_test
        assert wsi_buffer.m_cur_pos == int_value * 2

        # newSize = mCurPos + testedValue;
        m_buffer_test = [0] * 100
        m_buffer_test[0] = 1
        m_buffer_test[1] = 2
        m_buffer_test[2] = 3

        wsi_buffer = WsiBuffer.init_by_buffer(m_buffer_test)
        m_cur_pos_test = 7
        wsi_buffer.m_cur_pos = m_cur_pos_test
        int_value = 1300
        m_alloc_size_test = wsi_buffer.m_cur_pos + int_value
        tested_array = [0] * m_alloc_size_test
        tested_array = m_buffer_test[:wsi_buffer.m_cur_pos] + tested_array[wsi_buffer.m_cur_pos:]
        wsi_buffer.align_to(int_value)
        assert wsi_buffer.get_buffer_internal() == tested_array
        assert wsi_buffer.get_buf_size() == m_alloc_size_test
        assert wsi_buffer.m_cur_pos == (int((m_cur_pos_test / int_value)) * int_value) + int_value

    def test_clear(self):
        wsi_buffer = WsiBuffer()
        m_buffer_test = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
        m_cur_pos_test = 7
        m_base_test = 10
        wsi_buffer.set_buffer_by_buffer(m_buffer_test)
        wsi_buffer.m_cur_pos = m_cur_pos_test
        wsi_buffer.set_base(m_base_test)
        wsi_buffer.clear()
        assert wsi_buffer.get_buffer_internal() == []
        assert wsi_buffer.m_cur_pos == 0
        assert wsi_buffer.get_base() == 0

    def test_ensure_space(self):
        tested_value = 1024
        n_test = 10
        m_buffer_test = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
        wsi_buffer = WsiBuffer.init_by_buf_size(tested_value)
        wsi_buffer.set_buffer_by_buffer(m_buffer_test)
        wsi_buffer.ensure_space(n_test)
        assert wsi_buffer.get_buffer_internal() == m_buffer_test

        # newSize = mAllocSize + mReallocSize
        tested_value = 7
        wsi_buffer.m_cur_pos = tested_value
        m_alloc_size_test = wsi_buffer.get_realloc_size() + wsi_buffer.get_buf_size()
        tested_array = [0] * m_alloc_size_test
        tested_array = m_buffer_test[:tested_value] + tested_array[tested_value:]
        wsi_buffer.ensure_space(tested_value)
        assert wsi_buffer.get_buffer_internal() == tested_array
        assert wsi_buffer.get_buf_size() == m_alloc_size_test

        # newSize = mCurPos + testedValue
        m_buffer_test = [0] * 100
        m_buffer_test[0] = 1
        m_buffer_test[1] = 2
        m_buffer_test[2] = 3

        wsi_buffer = WsiBuffer.init_by_buffer(m_buffer_test)
        m_cur_pos_test = 7
        wsi_buffer.m_cur_pos = m_cur_pos_test
        tested_value = 1300
        m_alloc_size_test = wsi_buffer.m_cur_pos + tested_value
        tested_array = [0] * m_alloc_size_test
        tested_array = m_buffer_test[:wsi_buffer.m_cur_pos] + tested_array[wsi_buffer.m_cur_pos:]
        wsi_buffer.ensure_space(tested_value)
        assert wsi_buffer.get_buffer_internal() == tested_array
        assert wsi_buffer.get_buf_size() == m_alloc_size_test

    def test_get_array_header(self):
        m_buffer_test = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
        wsi_buffer = WsiBuffer.init_by_buffer(m_buffer_test)
        tested_value = 10
        m_cur_pos_test = 0

        # 2 hardcode from getArrayHeader method
        wsi_buffer.m_cur_pos = tested_value
        m_realloc_size_test = wsi_buffer.get_realloc_size()
        tested_array = [0] * (m_realloc_size_test + tested_value + 2)

        assert wsi_buffer.get_array_header() == m_cur_pos_test
        assert wsi_buffer.m_ary_hdr_idx == tested_value
        tested_array = m_buffer_test[:tested_value] + tested_array[tested_value:]
        assert wsi_buffer.get_buffer_internal() == tested_array
        assert wsi_buffer.get_buf_size() == tested_value + 2 + m_realloc_size_test

    def test_get_array_header_exception(self):
        wsi_buffer = WsiBuffer()
        tested_value = 15
        m_cur_pos_test = 0
        wsi_buffer.m_cur_pos = tested_value
        with pytest.raises(Exception):
            assert wsi_buffer.get_array_header() == m_cur_pos_test

    def test_get_big_decimal(self):
        big_decimal = BigDecimal(123)
        bytes = [48, 48, 48, 48, 48, 48, 48, 49, 50, 51]
        wsi_buffer = WsiBuffer.init_by_buffer(bytes)
        precision = 10
        scale = big_decimal.get_scale()
        assert wsi_buffer.get_big_decimal_d_type_precision_scale(WsiBuffer.DTYPE_NU, precision, scale) == big_decimal

    def test_get_big_decimal_pos(self):
        tested_value = BigDecimal(123)
        m_pos_test = 3
        bytes = [48, 48, 48, 48, 48, 48, 48, 49, 50, 51]
        wsi_buffer = WsiBuffer.init_by_buffer(bytes)
        precision = 7
        scale = tested_value.get_scale()
        assert wsi_buffer.get_big_decimal_d_type_new_pos_precision_scale(WsiBuffer.DTYPE_NU, m_pos_test, precision,
                                                                         scale)

    def test_get_big_decimal_array(self):
        ar_size_test = 2
        big_decimals = [BigDecimal(1230), BigDecimal(1230)]
        bytes = [48, 48, 48, 48, 48, 48, 48, 49, 50, 51, 48, 48, 48, 48, 48, 48, 48, 49, 50, 51]
        wsi_buffer = WsiBuffer.init_by_buffer(bytes)
        precision = 10
        scale = 1
        assert wsi_buffer.get_big_decimal_array(WsiBuffer.DTYPE_NU, ar_size_test, precision, scale) == big_decimals

    def test_get_big_decimal_array_new_pos(self):
        ar_size_test = 2
        m_pos_test = 3
        big_decimals = [BigDecimal(1230), BigDecimal(0)]

        bytes = [48, 48, 48, 48, 48, 48, 48, 49, 50, 51, 48, 48, 48, 48, 48, 48, 48, 49, 50, 51]
        wsi_buffer = WsiBuffer.init_by_buffer(bytes)

        precision = 7
        scale = 1
        assert wsi_buffer.get_big_decimal_array_new_pos(WsiBuffer.DTYPE_NU, ar_size_test, m_pos_test, precision, scale) == big_decimals

    def test_get_big_integer(self):
        big_integer = 68051240283893381193397944223005683760
        bytes = [48, 48, 48, 48, 48, 48, 48, 49, 50, 51, 48, 48, 48, 49, 50, 51]
        wsi_buffer = WsiBuffer.init_by_buffer(bytes)
        assert wsi_buffer.get_big_integer_d_type(WsiBuffer.DTYPE_NU) == big_integer

    def test_get_big_integer_d_type_new_pos(self):
        big_integer = 68051240522198033477589114048117485616
        offset_test = 3
        bytes = [48, 48, 48, 48, 48, 48, 48, 49, 50, 51, 48, 48, 48, 49, 50, 51, 49, 50, 51]
        wsi_buffer = WsiBuffer.init_by_buffer(bytes)
        assert wsi_buffer.get_big_integer_d_type_new_pos(WsiBuffer.DTYPE_NU, offset_test) == big_integer

    def test_get_big_integer_array(self):
        ar_size_test = 2
        big_integers = [64053151420411960267759038102254923824, 64053212426406567057055335849479254320]
        bytes = [48, 48, 48, 48, 48, 48, 48, 49, 50, 51, 48, 48, 48, 48, 48, 48, 48, 49, 50, 51, 48, 48, 48, 48, 48, 48,
                 48, 49, 50, 51, 48, 48, 48, 48, 48, 48, 48, 49, 50, 51]
        wsi_buffer = WsiBuffer.init_by_buffer(bytes)
        assert wsi_buffer.get_big_integer_array(WsiBuffer.DTYPE_NU, ar_size_test) == big_integers

    def test_get_big_integer_array_new_pos(self):
        ar_size_test = 2
        new_pos_test = 3
        big_integers = [66716799708840312637131034997000515632, 64053151420415582304332597452386349107]
        bytes = [48, 48, 48, 48, 48, 48, 48, 49, 50, 51, 48, 48, 48, 48, 48, 48, 48, 49, 50, 51, 48, 48, 48, 48, 48, 48,
                 48, 49, 50, 51, 48, 48, 48, 48, 48, 48, 48, 49, 50, 51]
        wsi_buffer = WsiBuffer.init_by_buffer(bytes)
        assert wsi_buffer.get_big_integer_array_new_pos(WsiBuffer.DTYPE_NU, ar_size_test, new_pos_test) == big_integers

    def test_get_bool_d_type(self):
        wsi_buffer = WsiBuffer.init_by_buf_size(10)
        assert wsi_buffer.get_bool_d_type(WsiBuffer.DTYPE_NU) is False

        bytes = [48, 48, 48, 48, 48, 48, 48, 49, 50, 51]
        wsi_buffer.set_buffer_by_buffer(bytes)
        assert wsi_buffer.get_bool_d_type(WsiBuffer.DTYPE_NU) is True

    def test_get_bool_d_type_new_pos(self):
        new_pos_test = 3
        wsi_buffer = WsiBuffer.init_by_buf_size(10)
        assert wsi_buffer.get_bool_d_type_new_pos(WsiBuffer.DTYPE_NU, new_pos_test) is False

        bytes = [48, 48, 48, 48, 48, 48, 48, 49, 50, 51]
        wsi_buffer.set_buffer_by_buffer(bytes)
        assert wsi_buffer.get_bool_d_type_new_pos(WsiBuffer.DTYPE_NU, new_pos_test) is True

    def test_get_bool_array(self):
        array_size = 5
        booleans = [True, True, True, True, False]
        bytes = [48, 48, 48, 48, 0, 48, 48, 49, 50, 51]
        wsi_buffer = WsiBuffer.init_by_buffer(bytes)
        assert wsi_buffer.get_bool_array(WsiBuffer.DTYPE_NU, array_size) == booleans

    def test_get_bool_array_new_pos(self):
        array_size = 5
        new_pos_test = 1
        booleans = [False, False, False, False, True]
        bytes = [0, 0, 0, 0, 0, 48, 48, 49, 50, 51]
        wsi_buffer = WsiBuffer.init_by_buffer(bytes)
        assert wsi_buffer.get_bool_array_new_pos(WsiBuffer.DTYPE_NU, array_size, new_pos_test) == booleans

    def test_get_buffer(self):
        bytes = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
        wsi_buffer = WsiBuffer.init_by_buffer(bytes)
        assert wsi_buffer.get_buffer() == bytes

        tested_value = 4
        wsi_buffer.set_base(tested_value)
        bytes = [5, 6, 7, 8, 9, 0]
        assert wsi_buffer.get_buffer() == bytes

    def test_get_buffer_len(self):
        bytes = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
        tested_value = 11
        wsi_buffer = WsiBuffer.init_by_buffer(bytes)
        assert wsi_buffer.get_buffer_len(tested_value) == bytes

        bytes = [1, 2, 3]
        tested_value = 3
        wsi_buffer.m_cur_pos = 0
        assert wsi_buffer.get_buffer_len(tested_value) == bytes

    def test_get_buffer_start_pos_len(self):
        bytes = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
        tested_array = []
        start_pos = 11
        len = 5
        wsi_buffer = WsiBuffer.init_by_buffer(bytes)
        assert wsi_buffer.get_buffer_start_pos_len(start_pos, len) == tested_array

        start_pos = 3
        tested_array = [4, 5, 6, 7, 8]
        assert wsi_buffer.get_buffer_start_pos_len(start_pos, len) == tested_array

        len = 10
        tested_array = [4, 5, 6, 7, 8, 9, 0]
        assert wsi_buffer.get_buffer_start_pos_len(start_pos, len) == tested_array

    def test_get_buffer_internal(self):
        bytes = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
        wsi_buffer = WsiBuffer.init_by_buffer(bytes)
        assert wsi_buffer.get_buffer_internal() == bytes

    def test_get_buf_size(self):
        m_alloc_size_test = 10
        wsi_buffer = WsiBuffer.init_by_buf_size(m_alloc_size_test)
        assert wsi_buffer.get_buf_size() == m_alloc_size_test

    def test_get_byte(self):
        bytes = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
        array_index = 0
        wsi_buffer = WsiBuffer.init_by_buffer(bytes)
        assert wsi_buffer.get_byte() == bytes[array_index]

        array_index = 3
        wsi_buffer.m_cur_pos = array_index
        assert wsi_buffer.get_byte() == bytes[array_index]

    def test_get_byte_d_type(self):
        bytes = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
        array_index = 0
        wsi_buffer = WsiBuffer.init_by_buffer(bytes)
        assert wsi_buffer.get_byte_d_type(WsiBuffer.DTYPE_NU) == bytes[array_index]

        array_index = 3
        wsi_buffer.m_cur_pos = array_index
        assert wsi_buffer.get_byte_d_type(WsiBuffer.DTYPE_NU) == bytes[array_index]

    def test_get_byte_d_type_new_pos(self):
        bytes = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
        array_index = 0
        new_pos_test = 3
        tested_value = new_pos_test
        wsi_buffer = WsiBuffer.init_by_buffer(bytes)
        assert wsi_buffer.get_byte_d_type_new_pos(WsiBuffer.DTYPE_NU, new_pos_test) == bytes[array_index + new_pos_test]
        assert wsi_buffer.get_byte_d_type_new_pos(WsiBuffer.DTYPE_NU, new_pos_test) == bytes[tested_value]
        assert wsi_buffer.m_cur_pos == tested_value + 1

    def test_get_byte_array(self):
        bytes = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
        tested_array = [1, 2, 3, 4, 5]
        array_size = len(tested_array)
        wsi_buffer = WsiBuffer.init_by_buffer(bytes)
        assert wsi_buffer.get_byte_array(WsiBuffer.DTYPE_NU, array_size) == tested_array

    def test_get_byte_array_new_pos(self):
        bytes = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
        tested_array = [4, 5, 6, 7, 8]
        array_size = len(tested_array)
        new_pos_test = 3
        wsi_buffer = WsiBuffer.init_by_buffer(bytes)
        assert wsi_buffer.get_byte_array_new_pos(WsiBuffer.DTYPE_NU, array_size, new_pos_test)

    def test_get_calendar(self):
        bytes = [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        wsi_buffer_new = WsiBuffer.init_by_buffer(bytes)
        tested_value = datetime.datetime.fromtimestamp(65793)
        assert wsi_buffer_new.get_calendar() == tested_value

    def test_get_calendar_1(self):
        bytes = [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        wsi_buffer_1 = WsiBuffer.init_by_buffer(bytes)
        tested_value = datetime.datetime.fromtimestamp(16843009)
        assert wsi_buffer_1.get_calendar_d_type(WsiBuffer.DTYPE_O) == tested_value

    def test_get_calendar_2(self):
        bytes = [0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0]
        new_pos_test = 3
        wsi_buffer_1 = WsiBuffer.init_by_buffer(bytes)
        tested_value = datetime.datetime.fromtimestamp(16843009)
        assert wsi_buffer_1.get_calendar_d_type_new_pos(WsiBuffer.DTYPE_O, new_pos_test) == tested_value

    def test_get_calendar_array(self):
        bytes = [1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0]
        wsi_buffer_23 = WsiBuffer.init_by_buffer(bytes)
        calendars = [datetime.datetime.fromtimestamp(16843009), datetime.datetime.fromtimestamp(16843009),
                     datetime.datetime.fromtimestamp(16843009)]
        assert calendars == wsi_buffer_23.get_calendar_array(WsiBuffer.DTYPE_O, len(calendars))

    def test_get_calendar_array_1(self):
        bytes = [0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0]
        new_pos_test = 3
        wsi_buffer_23 = WsiBuffer.init_by_buffer(bytes)
        calendars = [datetime.datetime.fromtimestamp(16843009), datetime.datetime.fromtimestamp(16843009),
                     datetime.datetime.fromtimestamp(16843009)]
        assert calendars == wsi_buffer_23.get_calendar_array_new_pos(WsiBuffer.DTYPE_O, len(calendars), new_pos_test)

    def test_get_char(self):
        wsi_buffer = WsiBuffer()
        tested_value = ' '
        assert wsi_buffer.get_char() == tested_value

    def test_get_decimal_d_type_precision_scale(self):
        wsi_decimal = WsiDecimal("123")
        bytes = [48, 48, 48, 48, 48, 48, 48, 49, 50, 51]
        wsi_buffer = WsiBuffer.init_by_buffer(bytes)
        precision = 10
        scale = 0
        assert wsi_buffer.get_decimal_d_type_precision_scale(WsiBuffer.DTYPE_NU, precision,
                                                             scale).get_value() == wsi_decimal.get_value()

    def test_get_decimal_d_type_new_pos_precision_scale(self):
        wsi_decimal = WsiDecimal("123000")
        bytes = [48, 48, 48, 48, 48, 48, 48, 49, 50, 51, 48, 48, 48, 48, 48, 48, 48, 49, 50, 51]
        wsi_buffer = WsiBuffer.init_by_buffer(bytes)
        precision = 10
        scale = 0
        new_pos_test = 3
        assert wsi_buffer.get_decimal_d_type_new_pos_precision_scale(WsiBuffer.DTYPE_NU, new_pos_test, precision,
                                                                     scale).get_value() == wsi_decimal.get_value()

    def test_get_decimal_d_object(self):
        bytes = [48, 48, 48, 48, 48, 48, 48, 49, 50, 51]
        wsi_buffer = WsiBuffer.init_by_buffer(bytes)
        big_decimal = BigDecimal.init_from_str("123")
        wsi_decimal = WsiDecimal.init_from_bd_value_precision_scale_dectype(big_decimal, 10, 0, WsiBuffer.DTYPE_NU)
        assert wsi_buffer.get_decimal_d_object(wsi_decimal).get_value() == wsi_decimal.get_value()

    def test_get_decimal_array(self):
        array_size = 3
        wsi_decimals = [WsiDecimal("123"), WsiDecimal("123"), WsiDecimal("123")]
        bytes = [48, 48, 48, 48, 48, 48, 48, 49, 50, 51, 48, 48, 48, 48, 48, 48, 48, 49, 50, 51, 48, 48, 48, 48, 48, 48,
                 48, 49, 50, 51]
        wsi_buffer = WsiBuffer.init_by_buffer(bytes)
        precision = 10
        scale = 0
        result = wsi_buffer.get_decimal_array(WsiBuffer.DTYPE_NU, array_size, precision, scale)
        for i in range(array_size):
            assert result[i].get_value() == wsi_decimals[i].get_value()

    def test_get_decimal_array_new_pos(self):
        array_size = 3
        wsi_decimals = [WsiDecimal("123000"), WsiDecimal("123000"), WsiDecimal("123000")]
        bytes = [48, 48, 48, 48, 48, 48, 48, 49, 50, 51, 48, 48, 48, 48, 48, 48, 48, 49, 50, 51, 48, 48, 48, 48, 48, 48,
                 48, 49, 50, 51, 48, 48, 48, 48, 48, 48, 48, 49, 50, 51]
        wsi_buffer = WsiBuffer.init_by_buffer(bytes)
        precision = 10
        scale = 0
        new_pos_test = 3
        result = wsi_buffer.get_decimal_array_new_pos(WsiBuffer.DTYPE_NU, array_size, new_pos_test, precision, scale)
        for i in range(array_size):
            assert result[i].get_value() == wsi_decimals[i].get_value()

    def test_get_double_d_type(self):
        tested_value = 3.2506E-319
        bytes = [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1]
        wsi_buffer = WsiBuffer.init_by_buffer(bytes)
        assert wsi_buffer.get_double_d_type(WsiBuffer.DTYPE_NU) == tested_value

    def test_get_double_d_type_new_pos(self):
        tested_value = 0.0
        bytes = [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1]
        wsi_buffer = WsiBuffer.init_by_buffer(bytes)
        new_pos_test = 3
        assert wsi_buffer.get_double_d_type_new_pos(WsiBuffer.DTYPE_NU, new_pos_test) == tested_value

    def test_get_double_array(self):
        doubles = [3.2506E-319, 7.748597204865478E-304, 3.2506E-319]
        array_size = 3
        bytes = [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1,
                 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1]
        wsi_buffer = WsiBuffer.init_by_buffer(bytes)
        result = wsi_buffer.get_double_array(WsiBuffer.DTYPE_NU, array_size)
        for i in range(array_size):
            assert result[i] == doubles[i]

    def test_get_double_array_new_pos(self):
        doubles = [0.0, 7.748604185488932E-304, 0.0]
        array_size = 3
        new_pos_test = 3
        bytes = [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1,
                 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1]
        wsi_buffer = WsiBuffer.init_by_buffer(bytes)
        result = wsi_buffer.get_double_array_new_pos(WsiBuffer.DTYPE_NU, array_size, new_pos_test)
        for i in range(array_size):
            assert result[i] == doubles[i]

    def test_get_dyn_string_array_elems(self):
        array_size = 1
        strings = [""]
        bytes = [1, 0, 0, 0, 0, 0, 0, 0]
        wsi_buffer = WsiBuffer.init_by_buffer(bytes)
        assert wsi_buffer.get_dyn_str_array_elems(array_size) == strings

    def test_get_dyn_string_array_elems_new_pos(self):
        array_size = 1
        new_pos_test = 3
        strings = [""]
        bytes = [1, 0, 0, 1, 0, 0, 0, 0]
        wsi_buffer = WsiBuffer.init_by_buffer(bytes)
        assert wsi_buffer.get_dyn_str_array_elems_new_pos(array_size, new_pos_test) == strings

    def test_get_float_d_type(self):
        tested_value = numpy.float32(3.04782416E-42)
        bytes = [127, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        wsi_buffer = WsiBuffer.init_by_buffer(bytes)
        result = wsi_buffer.get_float_d_type(WsiBuffer.DTYPE_NU)
        assert result == tested_value

    def test_get_float_d_type_new_pos(self):
        tested_value = numpy.float32(3.04782416E-42)
        new_pos_test = 3
        bytes = [0, 0, 0, 127, 8, 0, 0, 0, 0, 0, 0, 0, 0]
        wsi_buffer = WsiBuffer.init_by_buffer(bytes)
        result = wsi_buffer.get_float_d_type_new_pos(WsiBuffer.DTYPE_NU, new_pos_test)
        assert result == tested_value

    def test_get_float_array(self):
        arr_size = 2
        floats = [numpy.float32(3.04782416E-42), numpy.float32(7.67362712E-34)]
        bytes = [127, 8, 0, 0, 0, 0, 127, 8]
        wsi_buffer = WsiBuffer.init_by_buffer(bytes)
        assert wsi_buffer.get_float_array(WsiBuffer.DTYPE_NU, arr_size) == floats

    def test_get_float_array_new_pos(self):
        arr_size = 2
        new_pos_test = 3
        floats = [numpy.float32(3.04782416E-42), numpy.float32(7.67362712E-34)]
        bytes = [0, 0, 0, 127, 8, 0, 0, 0, 0, 127, 8]
        wsi_buffer = WsiBuffer.init_by_buffer(bytes)
        assert wsi_buffer.get_float_array_new_pos(WsiBuffer.DTYPE_NU, arr_size, new_pos_test) == floats

    def test_get_int(self):
        tested_value = 1
        bytes = [1, 0, 0, 0, 0, 0, 0, 0]
        wsi_buffer = WsiBuffer.init_by_buffer(bytes)
        assert wsi_buffer.get_int() == tested_value

    def test_get_int_d_type(self):
        tested_value = 1
        bytes = [1, 0, 0, 0, 0, 0, 0, 0]
        wsi_buffer = WsiBuffer.init_by_buffer(bytes)
        assert wsi_buffer.get_int_d_type(WsiBuffer.DTYPE_NU) == tested_value

    def test_get_int_d_type_new_pos(self):
        tested_value = 1
        new_pos_test = 3
        bytes = [1, 0, 0, 1, 0, 0, 0, 0]
        wsi_buffer = WsiBuffer.init_by_buffer(bytes)
        assert wsi_buffer.get_int_d_type_new_pos(WsiBuffer.DTYPE_NU, new_pos_test) == tested_value

    def test_get_int_array(self):
        array_size = 3
        ints = [1, 0, 1]
        bytes = [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]
        wsi_buffer = WsiBuffer.init_by_buffer(bytes)
        assert wsi_buffer.get_int_array(WsiBuffer.DTYPE_NU, array_size) == ints

    def test_get_int_array_new_pos(self):
        array_size = 3
        new_pos_test = 3
        ints = [1, 0, 1]
        bytes = [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]
        wsi_buffer = WsiBuffer.init_by_buffer(bytes)
        assert wsi_buffer.get_int_array_new_pos(WsiBuffer.DTYPE_NU, array_size, new_pos_test) == ints

    def test_get_long_d_type(self):
        bytes = [1, 0, 0, 0, 0, 0, 0, 0]
        wsi_buffer = WsiBuffer.init_by_buffer(bytes)
        tested_value = 1
        assert wsi_buffer.get_long_d_type(WsiBuffer.DTYPE_NU) == tested_value

    def test_get_long_d_type_new_pos(self):
        bytes = [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]
        wsi_buffer = WsiBuffer.init_by_buffer(bytes)
        tested_value = 1
        new_pos_test = 3
        assert wsi_buffer.get_long_d_type_new_pos(WsiBuffer.DTYPE_NU, new_pos_test) == tested_value

    def test_get_long_array(self):
        array_size = 2
        longs = [1, 1]
        bytes = [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]
        wsi_buffer = WsiBuffer.init_by_buffer(bytes)
        assert wsi_buffer.get_long_array(WsiBuffer.DTYPE_NU, array_size) == longs

    def test_get_long_array_new_pos(self):
        array_size = 2
        longs = [1, 1]
        bytes = [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]
        wsi_buffer = WsiBuffer.init_by_buffer(bytes)
        new_pos_test = 3
        assert wsi_buffer.get_long_array_new_pos(WsiBuffer.DTYPE_NU, array_size, new_pos_test) == longs

    def test_get_param_entry(self):
        tested_value = 1
        bytes = [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        wsi_buffer = WsiBuffer.init_by_buffer(bytes)
        assert wsi_buffer.get_param_entry() == tested_value

    def test_get_param_entry_phindex_paramcnt(self):
        tested_value = 1
        bytes = [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        wsi_buffer = WsiBuffer.init_by_buffer(bytes)
        wsi_buffer.m_cur_param_idx += 1
        assert wsi_buffer.get_param_entry_phindex_paramcnt(wsi_buffer.m_param_header,
                                                           wsi_buffer.m_cur_param_idx) == tested_value

    def test_get_param_header(self):
        m_param_header = 5
        m_cur_param_idx = 0
        wsi_buffer = WsiBuffer()
        wsi_buffer.get_param_header(m_param_header)
        assert wsi_buffer.m_param_header == m_param_header
        assert wsi_buffer.m_cur_param_idx == m_cur_param_idx

    def test_get_position(self):
        wsi_buffer = WsiBuffer()
        m_cur_pos = 10
        m_base = 5
        wsi_buffer.set_position(m_cur_pos)
        wsi_buffer.set_base(m_base)
        assert wsi_buffer.get_position() == (m_cur_pos - m_base)

    def test_get_realloc_size_test(self):
        wsi_buffer = WsiBuffer()
        tested_value = 1024
        assert wsi_buffer.get_realloc_size() == tested_value

    def test_get_short(self):
        bytes = [1, 0, 0, 0, 0, 0, 0, 0]
        tested_value = 1
        wsi_buffer = WsiBuffer.init_by_buffer(bytes)
        assert wsi_buffer.get_short() == tested_value

    def test_get_short_d_type(self):
        bytes = [1, 0, 0, 0, 0, 0, 0, 0]
        tested_value = 1
        wsi_buffer = WsiBuffer.init_by_buffer(bytes)
        assert wsi_buffer.get_short_d_type(WsiBuffer.DTYPE_NU) == tested_value

    def test_get_short_d_type_new_pos(self):
        bytes = [1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1]
        tested_value = 257
        new_pos_test = 3
        wsi_buffer = WsiBuffer.init_by_buffer(bytes)
        assert wsi_buffer.get_short_d_type_new_pos(WsiBuffer.DTYPE_NU, new_pos_test) == tested_value

    def test_get_short_array(self):
        bytes = [1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1]
        shorts = [1, 257]
        array_size = 2
        wsi_buffer = WsiBuffer.init_by_buffer(bytes)
        assert wsi_buffer.get_short_array(WsiBuffer.DTYPE_NU, array_size) == shorts

    def test_get_short_array_new_pos(self):
        bytes = [1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1]
        shorts = [257, 1]
        array_size = 2
        new_pos_test = 3
        wsi_buffer = WsiBuffer.init_by_buffer(bytes)
        assert wsi_buffer.get_short_array_new_pos(WsiBuffer.DTYPE_NU, array_size, new_pos_test) == shorts

    def test_get_string_len(self):
        bytes = [116, 101, 115, 116, 0, 0, 0, 0]
        wsi_buffer = WsiBuffer.init_by_buffer(bytes)
        tested_value = "test"
        len_test = 4
        assert wsi_buffer.get_str_len(len_test) == tested_value
        assert wsi_buffer.m_cur_pos == len_test

    def test_get_string_d_type_len(self):
        bytes = [116, 101, 115, 116, 0, 0, 0, 0]
        wsi_buffer = WsiBuffer.init_by_buffer(bytes)
        tested_value = "test"
        len_test = 4
        assert wsi_buffer.get_str_d_type_len(WsiBuffer.DTYPE_NU, len_test) == tested_value
        assert wsi_buffer.m_cur_pos == len_test

        bytes = [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1]
        wsi_buffer = WsiBuffer.init_by_buffer(bytes)
        tested_value = ""
        assert wsi_buffer.get_str_d_type_len(wsi_buffer.DTYPE_VT, len_test) == tested_value

    def test_get_string_d_type_new_pos_len(self):
        bytes = [10, 20, 30, 116, 101, 115, 116, 0, 0, 0, 0]
        wsi_buffer = WsiBuffer.init_by_buffer(bytes)
        tested_value = "test"
        len_test = 4
        new_pos_test = 3
        assert wsi_buffer.get_str_d_type_new_pos_len(WsiBuffer.DTYPE_NU, new_pos_test, len_test) == tested_value
        assert wsi_buffer.m_cur_pos == (len_test + new_pos_test)

    def test_get_string_array(self):
        array_size = 4
        len_test = 1
        strings = ["t", "e", "s", "t"]
        bytes = [116, 101, 115, 116, 0, 0, 0, 0]
        wsi_buffer = WsiBuffer.init_by_buffer(bytes)
        wsi_buffer.m_cur_pos = 0
        assert wsi_buffer.get_str_array(WsiBuffer.DTYPE_NU, array_size, len_test) == strings

    def test_get_string_array_new_pos(self):
        array_size = 4
        len_test = 1
        new_pos_test = 3
        strings = ["t", "e", "s", "t"]
        bytes = [40, 20, 10, 116, 101, 115, 116, 0, 0, 0, 0]
        wsi_buffer = WsiBuffer.init_by_buffer(bytes)
        wsi_buffer.m_cur_pos = 0
        assert wsi_buffer.get_str_array_new_pos(WsiBuffer.DTYPE_NU, array_size, new_pos_test, len_test) == strings

    def test_put_big_decimal_obj_d_type_len_scale(self):
        big_decimal = BigDecimal.init_from_str("123")
        wsi_buffer = WsiBuffer()
        bytes = [0] * wsi_buffer.get_realloc_size()
        tested_array = [49, 50, 51]
        bytes[wsi_buffer.m_cur_pos:len(tested_array)] = tested_array[:len(tested_array)]
        wsi_buffer.put_big_decimal_d_type_precision_scale(big_decimal, WsiBuffer.DTYPE_NU, big_decimal.get_precision(),
                                                          big_decimal.get_scale())
        assert wsi_buffer.get_buffer_internal() == bytes

    def test_put_big_decimal_obj_d_type_new_pos_len_scale(self):
        new_pos_test = 3
        big_decimal = BigDecimal.init_from_str("123")
        wsi_buffer = WsiBuffer()
        bytes = [0] * (wsi_buffer.get_realloc_size() + new_pos_test)
        tested_array = [0, 0, 0, 49, 50, 51]
        bytes[wsi_buffer.m_cur_pos:len(tested_array)] = tested_array[:len(tested_array)]
        wsi_buffer.put_big_decimal_d_type_new_pos_precision_scale(big_decimal, WsiBuffer.DTYPE_NU, new_pos_test,
                                                                  big_decimal.get_precision(), big_decimal.get_scale())

    def test_put_big_decimal_array(self):
        big_decimals = [BigDecimal(1234), BigDecimal(123)]
        bytes = [49, 50, 51, 52, 48, 49, 50, 51]
        precision = 4
        scale = 0
        wsi_buffer = WsiBuffer.init_by_buf_size(len(bytes))
        wsi_buffer.put_big_decimal_ary_d_type_len_scale(big_decimals, WsiBuffer.DTYPE_NU, precision, scale)
        assert wsi_buffer.get_buffer_internal() == bytes

    def test_put_big_decimal_ary_d_type_new_pos_len_scale(self):
        big_decimals = [BigDecimal(1234), BigDecimal(123)]
        tested_array = [0, 0, 0, 49, 50, 51, 52, 48, 49, 50, 51]
        precision = 4
        scale = 0
        new_pos_test = 3
        wsi_buffer = WsiBuffer()
        bytes = [0] * (wsi_buffer.get_realloc_size() + new_pos_test)
        bytes[wsi_buffer.m_cur_pos:wsi_buffer.m_cur_pos + len(tested_array)] = tested_array[:len(tested_array)]
        wsi_buffer.put_big_decimal_ary_d_type_new_pos_len_scale(big_decimals, WsiBuffer.DTYPE_NU, new_pos_test,
                                                                precision, scale)
        assert wsi_buffer.get_buffer_internal() == bytes

    def test_put_big_integer_obj_d_type(self):
        big_integer = 123
        wsi_buffer = WsiBuffer()
        tested_array = [123, 0, 0, 0, 0]
        bytes = [0] * wsi_buffer.get_realloc_size()
        bytes[wsi_buffer.m_cur_pos:wsi_buffer.m_cur_pos + len(tested_array)] = tested_array[:len(tested_array)]
        wsi_buffer.put_big_integer_d_type(big_integer, WsiBuffer.DTYPE_LU)
        assert wsi_buffer.get_buffer_internal() == bytes

    def test_put_big_integer_obj_d_type_new_pos(self):
        big_integer = 123
        new_pos_test = 3
        wsi_buffer = WsiBuffer()
        tested_array = [0, 0, 0, 123, 0, 0, 0, 0]
        bytes = [0] * (wsi_buffer.get_realloc_size() + new_pos_test)
        bytes[wsi_buffer.m_cur_pos:len(tested_array)] = tested_array[:len(tested_array)]
        wsi_buffer.put_big_integer_d_type_new_pos(big_integer, WsiBuffer.DTYPE_LU, new_pos_test)
        assert wsi_buffer.get_buffer_internal() == bytes

    def test_put_big_integer_ary_d_type(self):
        big_integers = [1234, 123]
        wsi_buffer = WsiBuffer()
        tested_array = [-46, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 123]
        bytes = [0] * wsi_buffer.get_realloc_size()
        bytes[wsi_buffer.m_cur_pos:wsi_buffer.m_cur_pos + len(tested_array)] = tested_array[:len(tested_array)]
        wsi_buffer.put_big_integer_ary_d_type(big_integers, WsiBuffer.DTYPE_NU)
        assert wsi_buffer.get_buffer_internal() == bytes

    def test_put_big_integer_ary_d_type_new_pos(self):
        big_integers = [1234, 123]
        wsi_buffer = WsiBuffer()
        tested_array = [0, 0, 0, -46, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 123]
        new_pos_test = 3
        bytes = [0] * (wsi_buffer.get_realloc_size() + new_pos_test)
        bytes[wsi_buffer.m_cur_pos:wsi_buffer.m_cur_pos + len(tested_array)] = tested_array[:len(tested_array)]
        wsi_buffer.put_big_integer_ary_d_type_new_pos(big_integers, WsiBuffer.DTYPE_NU, new_pos_test)
        assert wsi_buffer.get_buffer_internal() == bytes

    def test_put_bool_value_d_type(self):
        b = False
        array_size = 5
        bytes = [0, 0, 0, 0, 0]
        wsi_buffer = WsiBuffer.init_by_buf_size(array_size)
        wsi_buffer.put_bool_d_type(b, WsiBuffer.DTYPE_NU)
        assert wsi_buffer.get_buffer_internal() == bytes

        b = True
        wsi_buffer.m_cur_pos = 0
        bytes = [1, 0, 0, 0, 0]
        wsi_buffer.put_bool_d_type(b, WsiBuffer.DTYPE_NU)
        assert wsi_buffer.get_buffer_internal() == bytes

    def test_put_bool_value_d_type_new_pos(self):
        b = True
        array_size = 5
        new_pos_test = 3
        bytes = [0, 0, 0, 1, 0, 0, 0, 0]
        wsi_buffer = WsiBuffer.init_by_buf_size(array_size + new_pos_test)
        wsi_buffer.put_bool_d_type_new_pos(b, WsiBuffer.DTYPE_NU, new_pos_test)
        assert wsi_buffer.get_buffer_internal() == bytes

    def test_put_bool_ary_d_type(self):
        booleans = [False, True, False]
        bytes = [0, 1, 0]
        wsi_buffer = WsiBuffer.init_by_buf_size(len(bytes))
        wsi_buffer.put_bool_ary_d_type(booleans, WsiBuffer.DTYPE_NU)
        assert wsi_buffer.get_buffer_internal() == bytes

    def test_put_bool_ary_d_type_new_pos(self):
        booleans = [False, True, False]
        tested_array = [0, 0, 0, 0, 1, 0]
        new_pos_test = 3
        wsi_buffer = WsiBuffer()
        bytes = [0] * (wsi_buffer.get_realloc_size() + new_pos_test)
        bytes[wsi_buffer.m_cur_pos:len(tested_array)] = tested_array[:len(tested_array)]
        wsi_buffer.put_bool_ary_d_type_new_pos(booleans, WsiBuffer.DTYPE_NU, new_pos_test)
        assert wsi_buffer.get_buffer_internal() == bytes

    def test_put_byte_value(self):
        wsi_buffer = WsiBuffer.init_by_buf_size(5)
        b = 5
        bytes = [b, 0, 0, 0, 0]
        wsi_buffer.put_byte(b)
        assert wsi_buffer.get_buffer_internal() == bytes

    def test_put_byte_value_d_type(self):
        wsi_buffer = WsiBuffer.init_by_buf_size(5)
        b = 5
        bytes = [b, 0, 0, 0, 0]
        wsi_buffer.put_byte_d_type(b, wsi_buffer.DTYPE_NU)
        assert wsi_buffer.get_buffer_internal() == bytes

    def test_put_byte_test(self):
        b = 5
        new_pos_test = 3
        bytes = [0, 0, 0, b, 0]
        wsi_buffer = WsiBuffer.init_by_buf_size(len(bytes))
        wsi_buffer.put_byte_d_type_new_pos(b, wsi_buffer.DTYPE_NU, new_pos_test)
        assert wsi_buffer.get_buffer_internal() == bytes

    def test_put_byte_ary_d_type(self):
        bytes = [1, 2, 3, 4, 5]
        wsi_buffer = WsiBuffer.init_by_buf_size(len(bytes))
        wsi_buffer.put_byte_ary_d_type(bytes, WsiBuffer.DTYPE_NU)
        assert wsi_buffer.get_buffer_internal() == bytes

    def test_put_byte_ary_d_type_new_pos(self):
        tested_array = [1, 2, 3, 4, 5]
        new_pos_test = 2
        wsi_buffer = WsiBuffer()
        bytes = [0] * (wsi_buffer.get_realloc_size() + new_pos_test)
        bytes[new_pos_test:new_pos_test + len(tested_array)] = tested_array[:len(tested_array)]
        wsi_buffer.put_byte_ary_d_type_new_pos(tested_array, WsiBuffer.DTYPE_NU, new_pos_test)
        assert wsi_buffer.get_buffer_internal() == bytes

    def test_put_calendar(self):
        wsi_buffer = WsiBuffer()
        tested_value = 35066987
        bytes = [0] * wsi_buffer.get_realloc_size()
        bytes[0] = -69
        bytes[1] = 90
        bytes[2] = 23
        bytes[3] = 2
        wsi_buffer.put_calendar(datetime.datetime.fromtimestamp(tested_value))
        assert wsi_buffer.get_buffer_internal() == bytes

    def test_put_calendar_2(self):
        wsi_buffer = WsiBuffer()
        tested_value = 35066987
        bytes = [0] * wsi_buffer.get_realloc_size()
        bytes[0] = -69
        bytes[1] = 90
        bytes[2] = 23
        bytes[3] = 2
        wsi_buffer.put_calendar_d_type(datetime.datetime.fromtimestamp(tested_value), WsiBuffer.DTYPE_NU)
        assert wsi_buffer.get_buffer_internal() == bytes

    def test_put_calendar_3(self):
        array_size = 10
        wsi_buffer = WsiBuffer()
        tested_value = 35066987
        new_pos_test = 3
        bytes = [0] * (wsi_buffer.get_realloc_size() + new_pos_test)
        bytes[3] = -69
        bytes[4] = 90
        bytes[5] = 23
        bytes[6] = 2
        wsi_buffer.put_calendar_d_type_new_pos(datetime.datetime.fromtimestamp(tested_value), WsiBuffer.DTYPE_NU,
                                               new_pos_test)
        assert wsi_buffer.get_buffer_internal() == bytes

    def test_put_calendar_array(self):
        tested_value = 35066987
        calendars = [datetime.datetime.fromtimestamp(tested_value), datetime.datetime.fromtimestamp(tested_value)]
        wsi_buffer = WsiBuffer()
        bytes = [0] * wsi_buffer.get_realloc_size()
        bytes[0] = -69
        bytes[1] = 90
        bytes[2] = 23
        bytes[3] = 2
        bytes[8] = -69
        bytes[9] = 90
        bytes[10] = 23
        bytes[11] = 2
        wsi_buffer.put_calendar_ary_d_type(calendars, WsiBuffer.DTYPE_NU)
        assert wsi_buffer.get_buffer_internal() == bytes

    def test_put_calendar_array_2(self):
        tested_value = 35066987
        new_pos_test = 3
        calendars = [datetime.datetime.fromtimestamp(tested_value), datetime.datetime.fromtimestamp(tested_value)]
        wsi_buffer = WsiBuffer()
        bytes = [0] * (wsi_buffer.get_realloc_size() + new_pos_test)
        bytes[3] = -69
        bytes[4] = 90
        bytes[5] = 23
        bytes[6] = 2
        bytes[11] = -69
        bytes[12] = 90
        bytes[13] = 23
        bytes[14] = 2
        wsi_buffer.put_calendar_ary_d_type_new_pos(calendars, WsiBuffer.DTYPE_NU, new_pos_test)
        assert wsi_buffer.get_buffer_internal() == bytes

    def test_put_char_value_d_type(self):
        tested_value = 'q'
        wsi_buffer = WsiBuffer()
        bytes = [0] * wsi_buffer.get_realloc_size()
        bytes[0] = 113
        wsi_buffer.put_char_d_type(tested_value, WsiBuffer.DTYPE_NU)
        assert wsi_buffer.get_buffer_internal() == bytes

    def test_put_char_value_d_type_new_pos(self):
        tested_value = 'q'
        wsi_buffer = WsiBuffer()
        new_pos_test = 3
        bytes = [0] * (wsi_buffer.get_realloc_size() + new_pos_test)
        bytes[3] = 113
        wsi_buffer.put_char_d_type_new_pos(tested_value, WsiBuffer.DTYPE_NU, new_pos_test)
        assert wsi_buffer.get_buffer_internal() == bytes

    def test_put_double_f_value_d_type(self):
        tested_value = 8.0
        wsi_buffer = WsiBuffer()
        bytes = [0] * wsi_buffer.get_realloc_size()
        bytes[6] = 32
        bytes[7] = 64
        wsi_buffer.put_double_d_type(tested_value, WsiBuffer.DTYPE_NU)
        assert wsi_buffer.get_buffer_internal() == bytes

    def test_put_double_f_value_d_type_new_pos(self):
        tested_value = 8.0
        new_pos_test = 3
        wsi_buffer = WsiBuffer()
        bytes = [0] * (wsi_buffer.get_realloc_size() + new_pos_test)
        bytes[9] = 32
        bytes[10] = 64
        wsi_buffer.put_double_d_type_new_pos(tested_value, WsiBuffer.DTYPE_NU, new_pos_test)
        assert wsi_buffer.get_buffer_internal() == bytes

    def test_put_double_ary_d_type(self):
        doubles = [10.0, 10.0, 10.0]
        wsi_buffer = WsiBuffer()
        bytes = [0] * wsi_buffer.get_realloc_size()
        bytes[6] = 36
        bytes[7] = 64
        bytes[14] = 36
        bytes[15] = 64
        bytes[22] = 36
        bytes[23] = 64
        wsi_buffer.put_double_ary_d_type(doubles, WsiBuffer.DTYPE_NU)
        assert wsi_buffer.get_buffer_internal() == bytes

    def test_put_double_ary_d_type_new_pos(self):
        doubles = [10.0, 10.0, 10.0]
        wsi_buffer = WsiBuffer()
        new_pos_test = 3
        bytes = [0] * (wsi_buffer.get_realloc_size() + new_pos_test)
        bytes[9] = 36
        bytes[10] = 64
        bytes[17] = 36
        bytes[18] = 64
        bytes[25] = 36
        bytes[26] = 64
        wsi_buffer.put_double_ary_d_type_new_pos(doubles, WsiBuffer.DTYPE_NU, new_pos_test)
        assert wsi_buffer.get_buffer_internal() == bytes

    def test_put_float_f_value_d_type(self):
        tested_value = float32(123.05)
        wsi_buffer = WsiBuffer()
        bytes = [0] * wsi_buffer.get_realloc_size()
        bytes[0] = -102
        bytes[1] = 25
        bytes[2] = -10
        bytes[3] = 66
        wsi_buffer.put_float_d_type(tested_value, WsiBuffer.DTYPE_NU)
        assert wsi_buffer.get_buffer_internal() == bytes

    def test_put_float_f_value_d_type_new_pos(self):
        tested_value = float32(123.05)
        wsi_buffer = WsiBuffer()
        new_pos_test = 3
        bytes = [0] * (wsi_buffer.get_realloc_size() + new_pos_test)
        bytes[3] = -102
        bytes[4] = 25
        bytes[5] = -10
        bytes[6] = 66
        wsi_buffer.put_float_d_type_new_pos(tested_value, WsiBuffer.DTYPE_NU, new_pos_test)
        assert wsi_buffer.get_buffer_internal() == bytes

    def test_put_float_ary_d_type(self):
        floats = [float32(123.05), float32(123.05), float32(123.05)]
        wsi_buffer = WsiBuffer()
        bytes = [0] * wsi_buffer.get_realloc_size()
        bytes[0] = -102
        bytes[1] = 25
        bytes[2] = -10
        bytes[3] = 66
        bytes[4] = -102
        bytes[5] = 25
        bytes[6] = -10
        bytes[7] = 66
        bytes[8] = -102
        bytes[9] = 25
        bytes[10] = -10
        bytes[11] = 66
        wsi_buffer.put_float_ary_d_type(floats, WsiBuffer.DTYPE_NU)
        assert wsi_buffer.get_buffer_internal() == bytes

    def test_put_float_array_d_type_new_pos(self):
        floats = [float32(123.05), float32(123.05), float32(123.05)]
        wsi_buffer = WsiBuffer()
        new_pos_test = 3
        bytes = [0] * (wsi_buffer.get_realloc_size() + new_pos_test)
        bytes[3] = -102
        bytes[4] = 25
        bytes[5] = -10
        bytes[6] = 66
        bytes[7] = -102
        bytes[8] = 25
        bytes[9] = -10
        bytes[10] = 66
        bytes[11] = -102
        bytes[12] = 25
        bytes[13] = -10
        bytes[14] = 66
        wsi_buffer.put_float_ary_d_type_new_pos(floats, WsiBuffer.DTYPE_NU, new_pos_test)
        assert wsi_buffer.get_buffer_internal() == bytes

    def test_put_int_value(self):
        i = 123
        wsi_buffer = WsiBuffer()
        bytes = [0] * wsi_buffer.get_realloc_size()
        bytes[0] = 123
        wsi_buffer.put_int(i)
        assert wsi_buffer.get_buffer_internal() == bytes

    def test_put_int_value_d_type(self):
        i = 123
        wsi_buffer = WsiBuffer()
        bytes = [0] * wsi_buffer.get_realloc_size()
        bytes[0] = 123
        wsi_buffer.put_int_d_type(i, WsiBuffer.DTYPE_NU)
        assert wsi_buffer.get_buffer_internal() == bytes

    def test_put_int_value_d_type_new_pos(self):
        i = 123
        new_pos_test = 3
        wsi_buffer = WsiBuffer()
        bytes = [0] * (wsi_buffer.get_realloc_size() + new_pos_test)
        bytes[3] = 123
        wsi_buffer.put_int_d_type_new_pos(i, WsiBuffer.DTYPE_NU, new_pos_test)
        assert wsi_buffer.get_buffer_internal() == bytes

    def test_put_int_ary_d_type(self):
        ints = [1, 2, 3, 4, 5, 6, 7, 8]
        wsi_buffer = WsiBuffer()
        bytes = [0] * wsi_buffer.get_realloc_size()
        bytes[0] = 1
        bytes[4] = 2
        bytes[8] = 3
        bytes[12] = 4
        bytes[16] = 5
        bytes[20] = 6
        bytes[24] = 7
        bytes[28] = 8
        wsi_buffer.put_int_ary_d_type(ints, WsiBuffer.DTYPE_NU)
        assert wsi_buffer.get_buffer_internal() == bytes

    def test_put_int_ary_d_type_new_pos(self):
        ints = [1, 2, 3, 4, 5, 6, 7, 8]
        wsi_buffer = WsiBuffer()
        new_pos_test = 3
        bytes = [0] * (wsi_buffer.get_realloc_size() + new_pos_test)
        bytes[3] = 1
        bytes[7] = 2
        bytes[11] = 3
        bytes[15] = 4
        bytes[19] = 5
        bytes[23] = 6
        bytes[27] = 7
        bytes[31] = 8
        wsi_buffer.put_int_ary_d_type_new_pos(ints, WsiBuffer.DTYPE_NU, new_pos_test)
        assert wsi_buffer.get_buffer_internal() == bytes

    def test_put_long_value_d_type(self):
        l = 12312312312312
        wsi_buffer = WsiBuffer()
        bytes = [0] * wsi_buffer.get_realloc_size()
        bytes[0] = -8
        bytes[1] = 113
        bytes[2] = 0
        bytes[3] = -81
        bytes[4] = 50
        bytes[5] = 11
        wsi_buffer.put_long_d_type(l, WsiBuffer.DTYPE_NU)
        assert wsi_buffer.get_buffer_internal() == bytes

    def test_put_long_value_d_type_new_pos(self):
        l = 12312312312312
        wsi_buffer = WsiBuffer()
        new_pos_test = 3
        bytes = [0] * (wsi_buffer.get_realloc_size() + new_pos_test)
        bytes[3] = -8
        bytes[4] = 113
        bytes[5] = 0
        bytes[6] = -81
        bytes[7] = 50
        bytes[8] = 11
        wsi_buffer.put_long_d_type_new_pos(l, WsiBuffer.DTYPE_NU, new_pos_test)
        assert wsi_buffer.get_buffer_internal() == bytes

    def test_put_long_ary_d_type(self):
        longs = [12312312312312, 12312312312312]
        wsi_buffer = WsiBuffer()
        bytes = [0] * wsi_buffer.get_realloc_size()
        bytes[0] = -8
        bytes[1] = 113
        bytes[2] = 0
        bytes[3] = -81
        bytes[4] = 50
        bytes[5] = 11
        bytes[6] = 0
        bytes[7] = 0
        bytes[8] = -8
        bytes[9] = 113
        bytes[10] = 0
        bytes[11] = -81
        bytes[12] = 50
        bytes[13] = 11
        wsi_buffer.put_long_ary_d_type(longs, WsiBuffer.DTYPE_NU)
        assert wsi_buffer.get_buffer_internal() == bytes

    def test_put_long_ary_d_type_new_pos(self):
        longs = [12312312312312, 12312312312312]
        wsi_buffer = WsiBuffer()
        new_pos_test = 3
        bytes = [0] * (wsi_buffer.get_realloc_size() + new_pos_test)
        bytes[3] = -8
        bytes[4] = 113
        bytes[5] = 0
        bytes[6] = -81
        bytes[7] = 50
        bytes[8] = 11
        bytes[9] = 0
        bytes[10] = 0
        bytes[11] = -8
        bytes[12] = 113
        bytes[13] = 0
        bytes[14] = -81
        bytes[15] = 50
        bytes[16] = 11
        wsi_buffer.put_long_ary_d_type_new_pos(longs, WsiBuffer.DTYPE_NU, new_pos_test)
        assert wsi_buffer.get_buffer_internal() == bytes

    def test_set_base(self):
        array = [1, 1, 0, 0, 0, 0, 0, 0]
        wsi_buffer = WsiBuffer.init_by_buffer(array)
        new_base = 5
        wsi_buffer.set_base(new_base)
        assert wsi_buffer.get_base() == new_base

    def test_set_base_exception(self):
        array = [1, 1, 0]
        wsi_buffer = WsiBuffer.init_by_buffer(array)
        new_base = 7
        with pytest.raises(Exception):
            wsi_buffer.set_base(new_base)

    def test_set_buffer_by_buffer(self):
        new_buffer = [1, 3, 7, 9]
        wsi_buffer = WsiBuffer()
        wsi_buffer.set_buffer_by_buffer(new_buffer)
        assert wsi_buffer.get_base() == 0
        assert wsi_buffer.get_position() == 0
        assert wsi_buffer.get_buf_size() == len(new_buffer)
        received_buffer = wsi_buffer.get_buffer()
        for i in range(len(received_buffer)):
            assert received_buffer[i] == new_buffer[i]

    def test_set_buffer_by_buffer_empty(self):
        null_buffer = []
        wsi_buffer = WsiBuffer()
        wsi_buffer.set_buffer_by_buffer(null_buffer)
        assert wsi_buffer.get_base() == 0
        assert wsi_buffer.get_position() == 0
        assert wsi_buffer.get_buf_size() == 0

    def test_set_buffer_by_buffer_buf_base(self):
        new_buffer = [1, 3, 7, 9, 11, 13]
        tested_base = 4
        wsi_buffer = WsiBuffer()
        wsi_buffer.set_buffer_by_buffer_buf_base(new_buffer, tested_base)
        assert wsi_buffer.get_buf_size() == len(new_buffer)
        assert wsi_buffer.get_base() == tested_base
        assert wsi_buffer.get_position() == 0

        recieved_buffer = wsi_buffer.get_buffer()
        for i in range(len(recieved_buffer)):
            assert recieved_buffer[i] == new_buffer[i + tested_base]

    def test_set_buffer_exception(self):
        new_buffer = [1, 3, 7]
        tested_base = 7
        wsi_buffer = WsiBuffer()
        with pytest.raises(Exception):
            wsi_buffer.set_buffer_by_buffer_buf_base(new_buffer, tested_base)

    def test_set_buf_size(self):
        buffer = [1, 3, 7]
        tested_buffer = [1, 3, 7, 0, 0, 0, 0, 0, 0, 0]
        new_size = 10
        wsi_buffer = WsiBuffer.init_by_buffer(buffer)
        wsi_buffer.m_cur_pos = len(buffer)
        wsi_buffer.set_buf_size(new_size)
        recieved_buffer = wsi_buffer.get_buffer()
        assert wsi_buffer.get_buf_size() == new_size
        for i in range(len(tested_buffer)):
            assert recieved_buffer[i] == tested_buffer[i]

    def test_set_buf_size_2(self):
        buffer = [1, 3, 7]
        tested_buffer = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        new_size = 10
        wsi_buffer = WsiBuffer.init_by_buffer(buffer)
        wsi_buffer.set_buf_size(new_size)
        recieved_buffer = wsi_buffer.get_buffer()
        assert wsi_buffer.get_buf_size() == new_size
        for i in range(len(tested_buffer)):
            assert recieved_buffer[i] == tested_buffer[i]

    def test_set_buf_size_3(self):
        buffer = [1, 3, 7]
        new_size = 10
        wsi_buffer = WsiBuffer.init_by_buffer(buffer)
        wsi_buffer.m_cur_pos = new_size
        wsi_buffer.set_buf_size(new_size)
        recieved_buffer = wsi_buffer.get_buffer()
        assert wsi_buffer.get_buf_size() == len(buffer)
        for i in range(len(buffer)):
            assert recieved_buffer[i] == buffer[i]

    def test_set_buf_size_exception(self):
        buffer = [1, 3, 7]
        new_size = 2
        wsi_buffer = WsiBuffer.init_by_buffer(buffer)
        wsi_buffer.m_cur_pos = len(buffer)
        with pytest.raises(Exception):
            wsi_buffer.set_buf_size(new_size)

    def test_set_position(self):
        buffer = [1, 3, 7, 9, 11, 33, 77, 99]
        wsi_buffer = WsiBuffer.init_by_buffer(buffer)
        new_pos = 5
        wsi_buffer.set_position(new_pos)
        assert wsi_buffer.get_position() == new_pos

    def test_set_position2(self):
        buffer = [1, 3, 7, 9, 11, 33, 77, 99]
        wsi_buffer = WsiBuffer.init_by_buffer(buffer)
        new_pos = 11
        wsi_buffer.set_position(new_pos)
        recieved_buffer = wsi_buffer.get_buffer()
        assert wsi_buffer.get_buf_size() == new_pos + 1024
        assert wsi_buffer.get_position() == new_pos
        for b in recieved_buffer:
            assert b == 0

    def test_set_position_3(self):
        buffer = [1, 3, 7, 9, 11, 33, 77, 99]
        wsi_buffer = WsiBuffer.init_by_buffer(buffer)
        new_pos = 11
        wsi_buffer.m_cur_pos = len(buffer)
        wsi_buffer.set_position(new_pos)
        assert wsi_buffer.get_position() == new_pos
        assert wsi_buffer.get_buf_size() == new_pos + 1024
        recieved_buffer = wsi_buffer.get_buffer()
        for i in range(len(recieved_buffer)):
            if i >= len(buffer):
                assert recieved_buffer[i] == 0
            else:
                assert recieved_buffer[i] == buffer[i]

    def test_set_position_exception(self):
        buffer = [1, 3, 7, 9, 11, 33, 77, 99]
        wsi_buffer = WsiBuffer.init_by_buffer(buffer)
        new_pos = 11
        wsi_buffer.set_base(1)
        with pytest.raises(Exception):
            wsi_buffer.set_position(new_pos)

    def test_set_realloc_size(self):
        wsi_buffer = WsiBuffer()
        tested_size = 100
        wsi_buffer.set_realloc_size(tested_size)
        assert wsi_buffer.get_realloc_size() == tested_size

    def test_set_realloc_size_exception(self):
        wsi_buffer = WsiBuffer()
        tested_size = -100
        with pytest.raises(Exception):
            wsi_buffer.set_realloc_size(tested_size)

    def test_put_short_value(self):
        s = 100
        wsi_buffer = WsiBuffer()
        bytes = [0] * wsi_buffer.get_realloc_size()
        bytes[0] = 100
        wsi_buffer.put_short(s)
        assert wsi_buffer.get_buffer_internal() == bytes

    def test_put_short_value_d_type(self):
        s = 100
        wsi_buffer = WsiBuffer()
        bytes = [0] * wsi_buffer.get_realloc_size()
        bytes[0] = 100
        wsi_buffer.put_short_d_type(s, WsiBuffer.DTYPE_NU)
        assert wsi_buffer.get_buffer_internal() == bytes

    def test_put_short(self):
        s = 100
        new_pos_test = 3
        wsi_buffer = WsiBuffer()
        bytes = [0] * (wsi_buffer.get_realloc_size() + new_pos_test)
        bytes[3] = 100
        wsi_buffer.put_short_d_type_new_pos(s, WsiBuffer.DTYPE_NU, new_pos_test)
        assert wsi_buffer.get_buffer_internal() == bytes

    def test_put_short_ary_d_type(self):
        shorts = [100, 100, 123]
        wsi_buffer = WsiBuffer()
        bytes = [0] * wsi_buffer.get_realloc_size()
        bytes[0] = 100
        bytes[2] = 100
        bytes[4] = 123
        wsi_buffer.put_short_ary_d_type(shorts, WsiBuffer.DTYPE_NU)
        assert wsi_buffer.get_buffer_internal() == bytes

    def test_put_short_array(self):
        shorts = [100, 100, 123]
        wsi_buffer = WsiBuffer()
        new_pos_test = 3
        bytes = [0] * (wsi_buffer.get_realloc_size() + new_pos_test)
        bytes[3] = 100
        bytes[5] = 100
        bytes[7] = 123
        wsi_buffer.put_short_ary_d_type_new_pos(shorts, WsiBuffer.DTYPE_NU, new_pos_test)
        assert wsi_buffer.get_buffer_internal() == bytes

    def test_put_str_value_null_term(self):
        s = "test"
        null_tarm_test = 3
        wsi_buffer = WsiBuffer()
        bytes = [0] * wsi_buffer.get_realloc_size()
        bytes[0] = 116
        bytes[1] = 101
        bytes[2] = 115
        bytes[3] = 116
        wsi_buffer.put_str_null_term(s, null_tarm_test)
        assert wsi_buffer.get_buffer_internal() == bytes

    def test_put_str_value_d_type_null_term(self):
        s = "test"
        null_term_test = 3
        wsi_buffer = WsiBuffer()
        bytes = [0] * wsi_buffer.get_realloc_size()
        bytes[0] = 116
        bytes[1] = 101
        bytes[2] = 115
        bytes[3] = 116
        wsi_buffer.put_str_d_type_null_term(s, WsiBuffer.DTYPE_NU, null_term_test)
        assert wsi_buffer.get_buffer_internal() == bytes

    def test_put_str_value_d_type_len_null_term(self):
        s = "test"
        null_term_test = 3
        len_test = 2
        wsi_buffer = WsiBuffer()
        bytes = [0] * wsi_buffer.get_realloc_size()
        bytes[0] = 116
        bytes[1] = 101
        wsi_buffer.put_str_d_type_len_null_term(s, WsiBuffer.DTYPE_NU, len_test, null_term_test)
        assert wsi_buffer.get_buffer_internal() == bytes

    def test_put_str_value_d_type_new_pos_len_null_term(self):
        s = "test"
        null_term_test = 3
        len_test = 2
        new_pos_test = 3
        wsi_buffer = WsiBuffer()
        bytes = [0] * (wsi_buffer.get_realloc_size() + new_pos_test)
        bytes[3] = 116
        bytes[4] = 101
        wsi_buffer.put_str_d_type_new_pos_len_null_term(s, WsiBuffer.DTYPE_NU, new_pos_test, len_test,
                                                        null_term_test)
        assert wsi_buffer.get_buffer_internal() == bytes

    def test_put_str_ary_d_type_len_null_term(self):
        strings = ["test", "test"]
        null_term_test = 3
        len_test = 5
        wsi_buffer = WsiBuffer()
        bytes = [0] * wsi_buffer.get_realloc_size()
        bytes[0] = 116
        bytes[1] = 101
        bytes[2] = 115
        bytes[3] = 116
        bytes[4] = 32
        bytes[5] = 116
        bytes[6] = 101
        bytes[7] = 115
        bytes[8] = 116
        bytes[9] = 32
        wsi_buffer.put_str_ary_d_type_len_null_term(strings, WsiBuffer.DTYPE_NU, len_test, null_term_test)
        assert wsi_buffer.get_buffer_internal() == bytes

    def test_put_str_ary_d_type_new_pos_len_null_term(self):
        strings = ["test", "test"]
        null_term_test = 3
        len_test = 5
        new_pos_test = 3
        wsi_buffer = WsiBuffer()
        bytes = [0] * (wsi_buffer.get_realloc_size() + new_pos_test)
        bytes[3] = 116
        bytes[4] = 101
        bytes[5] = 115
        bytes[6] = 116
        bytes[7] = 32
        bytes[8] = 116
        bytes[9] = 101
        bytes[10] = 115
        bytes[11] = 116
        bytes[12] = 32
        wsi_buffer.put_str_ary_d_type_new_pos_len_null_term(strings, WsiBuffer.DTYPE_NU, new_pos_test, len_test, null_term_test)
        assert wsi_buffer.get_buffer_internal() == bytes

    def test_put_wsi_array_obj(self):
        strings = ["test", "test"]
        wsi_buffer = WsiBuffer()
        bytes = [0] * wsi_buffer.get_realloc_size()
        wsi_array = WsiArray.init_by_all_vars(strings, wsi_buffer, WsiBuffer.DTYPE_T, 1, 1, 1, False, 1, "1", False)
        bytes[0] = 1
        bytes[2] = 14
        bytes[3] = 1
        bytes[4] = 32
        bytes[8] = 1
        bytes[10] = 64
        bytes[11] = 1
        bytes[12] = 2
        bytes[16] = 32
        bytes[20] = 1
        bytes[28] = 1
        wsi_buffer.put_wsi_array(wsi_array)
        assert wsi_buffer.get_buffer_internal() == bytes

    def test_put_wsi_array_new_pos(self):
        strings = ["test", "test"]
        wsi_buffer = WsiBuffer()
        new_pos_test = 3
        bytes = [0] * (wsi_buffer.get_realloc_size() + new_pos_test)
        wsi_array = WsiArray.init_by_all_vars(strings, wsi_buffer, WsiBuffer.DTYPE_T, 1, 1, 1, False, 1, "1", False)
        bytes[3] = 1
        bytes[5] = 14
        bytes[6] = 1
        bytes[7] = 48
        bytes[11] = 1
        bytes[13] = 64
        bytes[14] = 1
        bytes[15] = 2
        bytes[19] = 48
        bytes[23] = 1
        bytes[31] = 1
        wsi_buffer.put_wsi_array_new_pos(wsi_array, new_pos_test)
        assert wsi_buffer.get_buffer_internal() == bytes

    def test_put_wsi_buffer_size(self):
        array_size = 8
        size = 3
        wsi_buffer_first = WsiBuffer.init_by_buf_size(array_size)
        bytes = [1, 1, 1, 1, 1, 1, 1, 1]
        test_array = [1, 1, 1, 0, 0, 0, 0, 0]
        wsi_buffer_second = WsiBuffer.init_by_buffer(bytes)
        wsi_buffer_first.put_wsi_buffer_size(wsi_buffer_second, size)
        assert wsi_buffer_first.get_buffer_internal() == test_array

    def test_put_wsi_buffer_size_new_pos(self):
        size = 8
        new_pos_test = 3
        wsi_buffer_first = WsiBuffer()
        bytes = [1, 1, 1, 1, 1, 1, 1, 1]
        test_array = [0] * (wsi_buffer_first.get_realloc_size() + new_pos_test)
        test_array[3] = 1
        test_array[4] = 1
        test_array[5] = 1
        test_array[6] = 1
        test_array[7] = 1
        test_array[8] = 1
        test_array[9] = 1
        test_array[10] = 1
        wsi_buffer_second = WsiBuffer.init_by_buffer(bytes)
        wsi_buffer_first.put_wsi_buffer_size_new_pos(wsi_buffer_second, size, new_pos_test)
        assert wsi_buffer_first.get_buffer_internal() == test_array

    def test_put_wsi_decimal_obj(self):
        precision = 3
        scale = 0
        bytes = [1, 1, 1, 1, 1, 1, 1, 1]
        test_array = [49, 50, 51, 1, 1, 1, 1, 1]
        wsi_decimal = WsiDecimal.init_from_bd_value_precision_scale_dectype(BigDecimal.init_from_str("123"), precision,
                                                                            scale, WsiBuffer.DTYPE_NU)
        wsi_buffer = WsiBuffer.init_by_buffer(bytes)
        wsi_buffer.put_wsi_decimal(wsi_decimal)
        assert wsi_buffer.get_buffer_internal() == test_array

    def test_put_wsi_decimal_obj_d_type_len_scale(self):
        precision = 4
        scale = 0
        bytes = [1, 1, 1, 1, 1, 1, 1, 1]
        test_array = [48, 49, 50, 51, 1, 1, 1, 1]
        wsi_decimal = WsiDecimal(BigDecimal.init_from_str("123"))
        wsi_buffer = WsiBuffer.init_by_buffer(bytes)
        wsi_buffer.put_wsi_decimal_d_type_len_scale(wsi_decimal, WsiBuffer.DTYPE_NU, precision, scale)
        assert wsi_buffer.get_buffer_internal() == test_array

    def test_put_wsi_decimal_obj_d_type_new_pos_len_scale(self):
        precision = 3
        scale = 0
        new_pos_test = 3
        bytes = [1, 1, 1, 1, 1, 1, 1, 1]
        test_array = [1, 1, 1, 49, 50, 51, 1, 1]
        wsi_decimal = WsiDecimal(BigDecimal.init_from_str("123"))
        wsi_buffer = WsiBuffer.init_by_buffer(bytes)
        wsi_buffer.put_wsi_decimal_d_type_new_pos_len_scale(wsi_decimal, WsiBuffer.DTYPE_NU, new_pos_test,
                                                            precision, scale)
        assert wsi_buffer.get_buffer_internal() == test_array

    def test_put_wsi_decimal_array(self):
        precision = 3
        scale = 0
        wsi_decimals = [WsiDecimal("123"), WsiDecimal("123")]
        bytes = [1, 1, 1, 1, 1, 1, 1, 1]
        test_array = [49, 50, 51, 49, 50, 51, 1, 1]
        wsi_buffer = WsiBuffer.init_by_buffer(bytes)
        wsi_buffer.put_wsi_decimal_ary_d_type_len_scale(wsi_decimals, WsiBuffer.DTYPE_NU, precision, scale)
        assert wsi_buffer.get_buffer_internal() == test_array
        assert wsi_buffer.get_buffer_internal() == bytes

    def test_put_wsi_decimal_array_new_pos(self):
        precision = 3
        scale = 0
        new_pos_test = 3
        wsi_decimals = [WsiDecimal("123"), WsiDecimal("123")]
        bytes = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        test_array = [1, 1, 1, 49, 50, 51, 49, 50, 51, 1]
        wsi_buffer = WsiBuffer.init_by_buffer(bytes)
        wsi_buffer.put_wsi_decimal_ary_d_type_new_pos_len_scale(wsi_decimals, WsiBuffer.DTYPE_NU, new_pos_test, precision, scale)
        assert len(wsi_buffer.get_buffer_internal()) == len(test_array)

    def test_put_wsi_structure_obj_d_type(self):
        wsi_structure = WsiStructure()
        bytes_second = [0, 0, 0, 0, 0, 0, 0, 0]
        test_array = [1, 1, 1, 0, 0, 0, 0, 0]
        wsi_buffer_second = WsiBuffer.init_by_buffer(bytes_second)
        wsi_structure.struct_size = 3
        bytes = [1, 1, 1, 1, 1, 1, 1, 1]
        wsi_structure.set_buffer(WsiBuffer.init_by_buffer(bytes), 0)
        wsi_buffer_second.put_wsi_structure_d_type(wsi_structure, WsiBuffer.DTYPE_NU)
        assert wsi_buffer_second.get_buffer_internal() == test_array

    def test_put_wsi_structure_obj_d_type_new_pos(self):
        wsi_structure = WsiStructure()
        bytes_second = [0, 0, 0, 0, 0, 0, 0, 0]
        test_array = [0, 0, 0, 1, 1, 1, 0, 0]
        new_pos_test = 3
        wsi_buffer_second = WsiBuffer.init_by_buffer(bytes_second)
        wsi_structure.struct_size = 3
        bytes = [1, 1, 1, 1, 1, 1, 1, 1]
        wsi_structure.set_buffer(WsiBuffer.init_by_buffer(bytes), 0)
        wsi_buffer_second.put_wsi_structure_d_type_new_pos(wsi_structure, WsiBuffer.DTYPE_NU, new_pos_test)
        assert wsi_buffer_second.get_buffer_internal() == test_array

    def test_put_wsi_structure_ary_d_type(self):
        wsi_structure = WsiStructure()
        bytes = [1, 1, 1, 1, 1, 1, 1, 1]
        wsi_structure.set_buffer(WsiBuffer.init_by_buffer(bytes), 0)
        wsi_structures = [wsi_structure, wsi_structure]
        wsi_structures[0].struct_alignment = 3
        wsi_structures[0].struct_size = 2
        wsi_structures[1].struct_alignment = 3
        wsi_structures[1].struct_size = 2
        bytes_second = [123, 123, 123, 123, 123, 123, 123, 123]
        test_array = [1, 1, 123, 1, 1, 123, 123, 123]
        wsi_buffer_second = WsiBuffer.init_by_buffer(bytes_second)
        wsi_buffer_second.put_wsi_structure_ary_d_type(wsi_structures, WsiBuffer.DTYPE_NU)
        assert wsi_buffer_second.get_buffer_internal() == test_array

    def test_put_wsi_structure_ary_d_type_new_pos(self):
        wsi_structure = WsiStructure()
        bytes = [1, 1, 1, 1, 1, 1, 1, 1]
        wsi_structure.set_buffer(WsiBuffer.init_by_buffer(bytes), 0)
        wsi_structures = [wsi_structure, wsi_structure]
        wsi_structures[0].struct_alignment = 3
        wsi_structures[0].struct_size = 2
        wsi_structures[1].struct_alignment = 3
        wsi_structures[1].struct_size = 2
        new_pos_test = 3
        array_size = 1024
        bytes_second = [123, 123, 123, 123, 123, 123, 123, 123]
        m_buffer_test = [123, 123, 123, 0, 0, 0, 1, 1, 1, 1]
        test_array = [0] * (array_size + len(bytes_second))
        test_array[0:len(m_buffer_test)] = m_buffer_test[0:len(m_buffer_test)]
        wsi_buffer_second = WsiBuffer.init_by_buffer(bytes_second)
        wsi_buffer_second.put_wsi_structure_ary_d_type_new_pos(wsi_structures, WsiBuffer.DTYPE_NU, new_pos_test)
        assert wsi_buffer_second.get_buffer_internal() == test_array

    def test_put_wsi_v2_structure_test_1(self):
        from wsit.main.com.vsi.wsi.wsi_v2_structure import WsiV2Structure
        bytes = [123, 123, 123, 123, 123, 123, 123, 123]
        wsi_v2_structure = WsiV2Structure.init_by_struct_size_alignment_byte_array(3, 3, [1, 1, 1, 1, 1, 1, 1, 1])
        tested_array = [1, 1, 1, 123, 123, 123, 123, 123]
        wsi_buffer = WsiBuffer.init_by_buffer(bytes)
        wsi_buffer.put_wsi_v2_structure_d_type(wsi_v2_structure, WsiBuffer.DTYPE_NU)
        assert wsi_buffer.get_buffer_internal() == tested_array

    def test_put_wsi_v2_structure_test_2(self):
        from wsit.main.com.vsi.wsi.wsi_v2_structure import WsiV2Structure
        bytes = [123, 123, 123, 123, 123, 123, 123, 123]
        wsi_v2_structure = WsiV2Structure.init_by_struct_size_alignment_byte_array(3, 3, [1, 1, 1, 1, 1, 1, 1, 1])
        tested_array = [123, 123, 123, 1, 1, 1, 123, 123]
        wsi_buffer = WsiBuffer.init_by_buffer(bytes)
        new_pos_test = 3
        wsi_buffer.put_wsi_v2_structure_d_type_new_pos(wsi_v2_structure, WsiBuffer.DTYPE_NU, new_pos_test)
        assert wsi_buffer.get_buffer_internal() == tested_array

    def test_put_wsi_v2_structure_array_1(self):
        from wsit.main.com.vsi.wsi.wsi_v2_structure import WsiV2Structure
        wsi_v2_structure = WsiV2Structure.init_by_struct_size_alignment_byte_array(3, 3, [1, 1, 1, 1, 1, 1, 1, 1])
        array_size = 1024
        wsi_v2_structures = [wsi_v2_structure, wsi_v2_structure]
        bytes = [123, 123, 123, 123, 123, 123, 123, 123]
        tested_array = [0]*(len(bytes) + array_size)
        tested_array[0] = 1
        tested_array[1] = 1
        tested_array[2] = 1
        tested_array[6] = 1
        tested_array[7] = 1
        tested_array[8] = 1
        wsi_buffer = WsiBuffer.init_by_buffer(bytes)
        wsi_buffer.put_wsi_v2_structure_ary_d_type(wsi_v2_structures, WsiBuffer.DTYPE_NU)
        assert wsi_buffer.get_buffer_internal() == tested_array

    def test_put_wsi_v2_structure_array_2(self):
         from wsit.main.com.vsi.wsi.wsi_v2_structure import WsiV2Structure
         wsi_v2_structure = WsiV2Structure.init_by_struct_size_alignment_byte_array(3, 3, [1, 1, 1, 1, 1, 1, 1, 1])
         array_size = 1024
         wsi_v2_structures = [wsi_v2_structure, wsi_v2_structure]
         bytes = [123, 123, 123, 123, 123, 123, 123, 123]
         tested_array = [0] * (len(bytes) + array_size)
         tested_array[0] = 123
         tested_array[1] = 123
         tested_array[2] = 123
         tested_array[6] = 1
         tested_array[7] = 1
         tested_array[8] = 1
         tested_array[9] = 1
         tested_array[10] = 1
         tested_array[11] = 1
         wsi_buffer = WsiBuffer.init_by_buffer(bytes)
         new_pos_test = 3
         wsi_buffer.put_wsi_v2_structure_ary_d_type_new_pos(wsi_v2_structures, WsiBuffer.DTYPE_NU, new_pos_test)
         assert wsi_buffer.get_buffer_internal() == tested_array

    def test_put_dyn_string_array_ary(self):
        bytes = [1, 2, 3, 4]
        array_size = 1024
        wsi_buffer = WsiBuffer.init_by_buffer(bytes)
        strings = ["test"]
        tested_array = [0] * (array_size + len(bytes))
        tested_array[0] = 4
        tested_array[2] = 14
        tested_array[3] = 2
        tested_array[8] = 116
        tested_array[9] = 101
        tested_array[10] = 115
        tested_array[11] = 116
        wsi_buffer.put_dyn_str_array_ary(strings)
        assert wsi_buffer.get_buffer_internal() == tested_array

    def test_put_dyn_string_array_ary_new_pos(self):
        bytes = [1, 2, 3, 4]
        array_size = 1024
        new_pos_test = 3
        wsi_buffer = WsiBuffer.init_by_buffer(bytes)
        strings = ["test"]
        tested_array = [0] * (array_size + len(bytes))
        tested_array[0] = 4
        tested_array[2] = 14
        tested_array[3] = 2
        tested_array[4] = 3
        tested_array[8] = 116
        tested_array[9] = 101
        tested_array[10] = 115
        wsi_buffer.put_dyn_str_array_ary_new_pos(strings, new_pos_test)
        assert wsi_buffer.get_buffer_internal() == tested_array

    def test_put_fixup_entry(self):
        bytes = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        tested_array = [5, 0, 0, 0, 3, 0, 15, 0, 9, 10]
        wsi_buffer = WsiBuffer.init_by_buffer(bytes)
        d_type = WsiBuffer.DTYPE_NU
        offset = 3
        elements = 5
        wsi_buffer.put_fixup_entry(d_type, offset, elements)
        assert wsi_buffer.get_buffer_internal() == tested_array

    def test_put_param_entry(self):
        bytes = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        wsi_buffer = WsiBuffer.init_by_buffer(bytes)
        array_size = 1024
        tested_array = [0] * (array_size + len(bytes))
        d_type = WsiBuffer.DTYPE_NU
        d_class = 3
        size = 4
        scale = 0
        tested_array[0] = 4
        tested_array[2] = 15
        tested_array[3] = 3
        tested_array[9] = 4
        wsi_buffer.put_param_entry(d_type, d_class, size, scale)
        assert wsi_buffer.get_buffer_internal() == tested_array

    def test_put_param_entry_phindex_paramcnt(self):
        bytes = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        wsi_buffer = WsiBuffer.init_by_buffer(bytes)
        array_size = 1024
        tested_array = [0] * (array_size + len(bytes))
        phindex = 2
        param_cnt = 1
        d_type = WsiBuffer.DTYPE_NU
        d_class = 3
        size = 4
        scale = 0
        tested_array[0] = 1
        tested_array[1] = 2
        tested_array[2] = 4
        tested_array[4] = 15
        tested_array[5] = 3
        tested_array[11] = 4
        wsi_buffer.put_param_entry_phindex_paramcnt(phindex, param_cnt, d_type, d_class, size, scale)
        assert wsi_buffer.get_buffer_internal() == tested_array

    def test_put_param_header(self):
        bytes = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        wsi_buffer = WsiBuffer.init_by_buffer(bytes)
        tested_value = 0
        p_count_test = 5
        assert tested_value == wsi_buffer.put_param_header(p_count_test)

    def test_to_string(self):
        bytes = [1, 2, 3, 4, 5, 6, 7, 8]
        wsi_buffer = WsiBuffer.init_by_buffer(bytes)
        tested_value = "    WsiBuffer.mBuffer = " + str(
            wsi_buffer.get_buffer()) + "\n" + "    WsiBuffer.mBase = 0\n" + "    WsiBuffer.mAllocSize = 8\n" + "    WsiBuffer.mCurPos = 0\n"
        assert wsi_buffer.to_string() == tested_value

    def test_put_array_dim(self):
        bytes = [1, 2, 3, 4, 5, 6, 7, 8]
        array_size = 1035   # hardcode from WsiBuffer
        dim_cnt = 1
        dlower = 1
        dupper = 3
        tested_array = [0] * array_size
        tested_array[0] = 1
        tested_array[1] = 2
        tested_array[2] = 3
        tested_array[3] = 4
        tested_array[12] = 1    # elemsize
        tested_array[13] = 2    # elemsize
        tested_array[20] = 3    # dlower ws multivalue
        tested_array[24] = 3    # dupper
        wsi_buffer = WsiBuffer.init_by_buffer(bytes)
        wsi_buffer.put_array_dim(dim_cnt, dlower, dupper)
        assert wsi_buffer.get_buffer_internal() == tested_array

    def test_put_array_header(self):
        bytes = [1, 2, 3, 4]
        wsi_buffer = WsiBuffer.init_by_buffer(bytes)
        dtype = WsiBuffer.DTYPE_NU
        dclass = 3
        size = 4
        scale = 0
        dims = 1
        array_size = 1024
        rowcol = False
        test_array = [0] * (array_size + len(bytes))
        test_array[0] = 4
        test_array[2] = 15
        test_array[3] = 3
        test_array[4] = 32
        test_array[10] = 64
        test_array[11] = 1
        test_array[16] = 32
        wsi_buffer.put_array_header(dtype, dclass, size, scale, dims, rowcol)
        assert wsi_buffer.get_buffer_internal() == test_array
