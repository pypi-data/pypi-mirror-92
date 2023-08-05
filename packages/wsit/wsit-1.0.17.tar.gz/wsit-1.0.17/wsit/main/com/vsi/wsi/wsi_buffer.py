import datetime
from typing import List

import numpy

from wsit.main.com.vsi.wsi.big_decimal import BigDecimal
from wsit.main.com.vsi.wsi.wsi_decimal import WsiDecimal
from wsit.main.com.vsi.wsi.wsi_structure import WsiStructure
from wsit.main.com.vsi.wsi.wsi_utils import WsiUtils, IntegerTypes
from wsit.main.com.vsi.wsi.wsi_v2_structure import WsiV2Structure


class WsiBuffer:
    """
    #
 *  The following constants are used to identify specific OpenVMS datatypes.
 *
 *  Atomic data types:

 """
    DTYPE_Z = 0  # unspecified
    DTYPE_BU = 2  # byte (unsigned)  8-bit unsigned quantity
    DTYPE_WU = 3  # word (unsigned)  16-bit unsigned quantity
    DTYPE_LU = 4  # longword (unsigned)  32-bit unsigned quantity
    DTYPE_QU = 5  # quadword (unsigned)  64-bit unsigned quantity
    DTYPE_OU = 25  # octaword (unsigned)  128-bit unsigned quantity
    DTYPE_B = 6  # byte integer (signed)  8-bit signed 2's-complement integer
    DTYPE_W = 7  # word integer (signed)  16-bit signed 2's-complement integer
    DTYPE_L = 8  # longword integer (signed)  32-bit signed 2's-complement integer
    DTYPE_Q = 9  # quadword integer (signed)  64-bit signed 2's-complement integer
    DTYPE_O = 26  # octaword integer (signed)  128-bit signed 2's-complement integer
    DTYPE_F = 10  # F_floating  32-bit single-precision floating point
    DTYPE_D = 11  # D_floating  64-bit double-precision floating point
    DTYPE_G = 27  # G_floating  64-bit double-precision floating point
    DTYPE_H = 28  # H_floating  128-bit quadruple-precision floating point
    DTYPE_FC = 12  # F_floating complex
    DTYPE_DC = 13  # D_floating complex
    DTYPE_GC = 29  # G_floating complex
    DTYPE_HC = 30  # H_floating complex
    DTYPE_CIT = 31  # COBOL Intermediate Temporary

    #  String data types:

    DTYPE_T = 14  # character string  a single 8-bit character or a sequence of characters
    DTYPE_VT = 37  # varying character string  16-bit count, followed by a string
    DTYPE_NU = 15  # numeric string, unsigned
    DTYPE_NL = 16  # numeric string, left separate sign
    DTYPE_NLO = 17  # numeric string, left overpunched sign
    DTYPE_NR = 18  # numeric string, right separate sign
    DTYPE_NRO = 19  # numeric string, right overpunched sign
    DTYPE_NZ = 20  # numeric string, zoned sign
    DTYPE_P = 21  # packed decimal string
    DTYPE_V = 1  # aligned bit string
    DTYPE_VU = 34  # unaligned bit string

    #  IEEE data types:

    DTYPE_FS = 52  # IEEE float basic single S
    DTYPE_FT = 53  # IEEE float basic double T
    DTYPE_FSC = 54  # IEEE float basic single S complex
    DTYPE_FTC = 55  # IEEE float basic double T complex
    DTYPE_FX = 57  # IEEE float basic extended
    DTYPE_FXC = 58  # IEEE float complex extended

    #  Miscellaneous data types:

    DTYPE_ZI = 22  # sequence of instructions
    DTYPE_ZEM = 23  # procedure entry mask
    DTYPE_DSC = 24  # descriptor
    DTYPE_BPV = 32  # bound procedure value
    DTYPE_BLV = 33  # bound label value
    DTYPE_ADT = 35  # absolute date and time

    #  BridgeWorks specific data types:

    DTYPE_STRUCT = 77  # BWX Structure

    #  Constants for the various class types encountered

    CLASS_S = 1  # Static/Scalar
    CLASS_D = 2  # Dynamic String
    CLASS_A = 4  # Array
    CLASS_SD = 9  # Scaled Decimal
    CLASS_NCA = 10  # Non-Contiguous Array
    CLASS_VS = 11  # Variant String
    CLASS_VSA = 12  # Variant String Array

    __BYTE_BITS = 8

    # Creates new WsiBuffer buffer of size 0
    def __init__(self):
        # The private data members below are used to maintain internal state

        self.m_buffer = []
        self.__m_base = 0
        self.m_alloc_size = 0
        self.__m_realloc_size = 1024
        self.m_cur_pos = 0

        # Used in processing of Parameter entries within buffer
        self.m_param_header = 0
        self.m_cur_param_idx = 0

        # Used in processing of Arrays within the buffer
        self.m_ary_hdr_idx = 0
        self.m_cur_dsc_pos = 0

    """
    /**
    * Creates new WsiBuffer buffer of a given size
    */
    """

    @classmethod
    def init_by_buf_size(cls, buf_size: int) -> 'WsiBuffer':
        WsiUtils.check_type(buf_size, int)
        wsi_buffer_new = cls()
        wsi_buffer_new.m_buffer = [0] * buf_size
        wsi_buffer_new.m_alloc_size = buf_size
        return wsi_buffer_new

    """
    /**
    * Creates new WsiBuffer buffer using a given byte array
    */
    """

    @classmethod
    def init_by_buffer(cls, buffer: List[int]) -> 'WsiBuffer':
        WsiUtils.check_list_type_of_intervals(buffer, IntegerTypes.EXT_BYTE)
        wsi_buffer_new = cls()
        wsi_buffer_new.set_buffer_by_buffer(buffer)
        return wsi_buffer_new

    @classmethod
    def init_by_buffer_buf_base(cls, buffer: List[int], buf_base: int) -> 'WsiBuffer':
        wsi_buffer_new = cls()
        wsi_buffer_new.set_buffer_by_buffer_buf_base(buffer, buf_base)
        return wsi_buffer_new

    """
    /**
    * Creates new WsiBuffer buffer using a given WsiBuffer object
    * Copy Constructor...
    */
    """

    @classmethod
    def init_by_wsi_buffer(cls, obj: 'WsiBuffer') -> 'WsiBuffer':
        WsiUtils.check_instance(obj, WsiBuffer)
        wsi_buffer_new = cls()
        wsi_buffer_new.set_buffer_by_buffer(obj.get_buffer())
        return wsi_buffer_new

    @classmethod
    def init_by_wsi_buffer_buf_base(cls, obj: 'WsiBuffer', buf_base: int) -> 'WsiBuffer':
        wsi_buffer_new = cls()
        wsi_buffer_new.set_buffer_by_buffer_buf_base(obj.get_buffer_internal(), obj.get_base() + buf_base)
        return wsi_buffer_new

    """
    /**
    * Creates new WsiBuffer from a subset of another WsiBuffer
    */
    """

    @classmethod
    def init_by_wsi_buffer_start_pos_len(cls, obj: 'WsiBuffer', start_pos: int, len: int) -> 'WsiBuffer':
        WsiUtils.check_instance(obj, WsiBuffer)
        wsi_buffer_new = cls()
        wsi_buffer_new.set_buffer_by_buffer(obj.get_buffer_start_pos_len(start_pos, len))
        return wsi_buffer_new

    """
    /*****************************************************************
    *
    * The following methods manage the creation, destruction, resizing,
    * and general manipulation of the underlining stream buffer.
    *
    *****************************************************************/

    /**
     *  Change the internal buffer size.  The new size must be at least
     *  as large at the amount currently in use.
     *
     *  @param l    new size
     *
     *  @throws IllegalArgumentException    Attempt to reduce the buffer size.
     */
    """

    def set_buf_size(self, buf_size: int):
        WsiUtils.check_type(buf_size, int)
        if buf_size < self.m_cur_pos:
            raise ValueError("Attempt to shorten encoding buffer.")

        if buf_size > self.m_cur_pos:

            # We're extending the buffer.  Allocate a new array and copy the
            # active data.
            t = [0]*buf_size
            if self.m_cur_pos > 0:
                t = self.m_buffer[:self.m_cur_pos] + [0]*(buf_size-self.m_cur_pos)
            self.m_buffer = t
            self.m_alloc_size = buf_size

    """
    /**
     *  Retrieve the currently allocated array size
     *
     * @return  allocated size
     */
    """

    def get_buf_size(self) -> int:
        return self.m_alloc_size

    """
    /**
     *  Establish a new reallocation unit size.  This is the amount to
     *  increase the internal buffer by when it becomes full.
     *
     *  @param l        new reallocation increment amount.
     *
     *  @throws IllegalArgumentException    Attempt to set the reallocation
     *                                      size to a negative value.
     */
    """

    def set_realloc_size(self, realloc_size: int):
        WsiUtils.check_type(realloc_size, int)
        if realloc_size <= 0:
            raise ValueError("Reallocation increments must be greater than zero.")
        self.__m_realloc_size = realloc_size

    """    
    /**
     *  Retrieve the current reallocation amount.
     *
     *  @return reallocation amount.
     */
    """

    def get_realloc_size(self) -> int:
        return self.__m_realloc_size

    """
    /**
     *  Establish a new byte array to use as the input encoded data stream.
     *
     *  @param  buffer      new byte stream array to process
     */
    """

    def set_buffer_by_buffer(self, buffer: List[int]):
        WsiUtils.check_list_type_of_intervals(buffer, IntegerTypes.EXT_BYTE)
        self.m_buffer = buffer
        self.__m_base = 0
        self.m_cur_pos = 0
        if self.m_buffer != []:
            self.m_alloc_size = self.m_buffer.__len__()
        else:
            self.m_alloc_size = 0

    def set_buffer_by_buffer_buf_base(self, buffer: List[int], buf_base: int):
        WsiUtils.check_list_type_of_intervals(buffer, IntegerTypes.EXT_BYTE)
        WsiUtils.check_type(buf_base, int)
        self.m_buffer = buffer
        if self.m_buffer is not None:
            self.m_alloc_size = self.m_buffer.__len__()
        else:
            self.m_alloc_size = 0

        if buf_base > self.m_alloc_size:
            raise ValueError("Nested WsiBuffer asked to reference past end of buffer.")

        self.__m_base = buf_base
        self.m_cur_pos = buf_base

    """
    /**
     *  Retrieve the internal data buffer.
     *
     *  @return data buffer reference
     */
    """

    def get_buffer(self) -> List[int]:
        if self.__m_base == 0:
            return self.m_buffer

        # If this is a nested buffer, then we need to create a copy
        return self.get_buffer_start_pos_len(0, self.m_alloc_size - self.__m_base)

    """
    /**
     *  Retrieve the internal data buffer regardless of base.
     *     (this is used to avoid an object creation
     *  @return data buffer reference
     */
    """

    def get_buffer_internal(self) -> List[int]:
        return self.m_buffer

    """
    /**
     *  Obtain the number of bytes currently in use in the data buffer.
     *
     *  @return number of bytes in use.
     */
    """

    def get_position(self) -> int:
        return self.m_cur_pos - self.__m_base

    """
    /**
     *  Set the current position in use in the data buffer.
     *
     *  @return number of bytes in use.
     */
     """

    def set_position(self, new_pos: int):
        WsiUtils.check_type(new_pos, int)
        if self.__m_base + new_pos > self.m_alloc_size:
            if self.__m_base > 0:
                raise ValueError("Nested WsiBuffer asked to reference past end of buffer.")

            # We're extending the buffer.  Allocate a new array and copy the
            # active data
            t = [0]*(new_pos + self.__m_realloc_size)
            if self.m_cur_pos > 0:
                if len(self.m_buffer) > 0:
                    t[0:self.m_cur_pos] = self.m_buffer[0:self.m_cur_pos]
                else:
                    raise Exception("Buffer doesn't contain elements")
            self.m_buffer = t
            self.m_alloc_size = self.__m_base + new_pos + self.__m_realloc_size

        self.m_cur_pos = self.__m_base + new_pos

    """
    /**
     *  Reset the end of used buffer point to the start of the data buffer.
     */
    """

    def reset_position(self):
        self.m_cur_pos = self.__m_base

    """
     /**
     *  Return the base being used by this buffer object.
     */
    """

    def get_base(self) -> int:
        return self.__m_base

    """
    /**
     *  Set the base being used by this object.
     *
     *  @return number of bytes in use.
     */
    """

    def set_base(self, new_pos: int):
        WsiUtils.check_type(new_pos, int)
        if new_pos > self.m_alloc_size:
            raise ValueError("Nested WsiBuffer asked to reference past end of buffer.")
        self.__m_base = new_pos

    """
    /**
     *  Clear the internal state: release the currently allocated buffer
     *  and reset the in-use amount to zero.
     */
    """

    def clear(self):
        self.m_buffer = []
        self.m_cur_pos = 0
        self.m_alloc_size = 0
        self.__m_base = 0

    """
    /**
     *  Ensure that sufficient free space exists in the data buffer.  This
     *  routine will, if necessary, allocate a new buffer, and copy forward
     *  the currently filled data.
     *
     *  <p>
     *  The new size of the buffer is only guarenteed to have 'n' free bytes.
     *  However, the buffer may be extended by more than that, depending on
     *  the reallocation chunk size.
     *
     *  @param  n       amount of free space to guarentee.
     */
    """

    def ensure_space(self, n: int):
        if self.m_cur_pos + n > self.m_alloc_size:
            if self.__m_base > 0:
                raise ValueError("Nested WsiBuffer asked to reference past end of buffer.")

            if self.m_cur_pos + n > self.m_alloc_size + self.__m_realloc_size:
                new_size = self.m_cur_pos + n
            else:
                new_size = self.m_alloc_size + self.__m_realloc_size

            t = [0] * new_size
            if self.m_cur_pos > 0:
                t = self.m_buffer[:self.m_cur_pos] + t[self.m_cur_pos:]

            self.m_buffer = t
            self.m_alloc_size = new_size

    """
    /*****************************************************************
    *
    * The following are insertion methods for the various entities that
    * can be put into a WsiBuffer.  These include headers, primitives,
    * padding, arrays, structures, and other WsiBuffers.
    *
    *****************************************************************/


    /*
     * putParamHeader inserts a parameter header into the Stream buffer.
     *    The built header has the exact same layout as a Scaled Decimal
     *    Descriptor on OpenVMS.
     */
   """

    def put_param_header(self, p_count: int) -> int:
        WsiUtils.check_type(p_count, int)
        phidx = self.m_cur_pos
        self.ensure_space(p_count * 12)  # Ensure space for parameter header
        self.m_cur_pos += p_count * 12
        self.m_param_header = phidx
        self.m_cur_param_idx = 0
        return phidx

    def put_param_entry(self, d_type: int, d_class: int, size: int, scale: int):
        self.m_cur_param_idx += 1
        self.put_param_entry_phindex_paramcnt(self.m_param_header, self.m_cur_param_idx, d_type, d_class, size, scale)

    def put_param_entry_phindex_paramcnt(self, phindex: int, paramcnt: int, d_type: int, d_class: int, size: int,
                                         scale: int):
        WsiUtils.check_type(phindex, int)
        WsiUtils.check_type(paramcnt, int)
        WsiUtils.check_type(d_type, int)
        WsiUtils.check_type(d_class, int)
        WsiUtils.check_type(size, int)
        WsiUtils.check_type(scale, int)

        self.m_param_header = phindex
        self.m_cur_param_idx = paramcnt
        #  don't align array header information
        if d_class != WsiBuffer.CLASS_A and d_class != WsiBuffer.CLASS_NCA and d_class != WsiBuffer.CLASS_VSA:
            self.align_to(self.__get_type_alignment(d_type))

        save_cur_pos = self.m_cur_pos
        self.set_position(phindex + (paramcnt - 1) * 12)
        self.put_short(size & 0xffff)  # length
        self.put_byte(d_type)  # data type
        self.put_byte(d_class)  # class type
        self.put_int(save_cur_pos)  # address field

        if d_type in [WsiBuffer.DTYPE_NU, WsiBuffer.DTYPE_NL, WsiBuffer.DTYPE_NLO, WsiBuffer.DTYPE_NR,
                      WsiBuffer.DTYPE_NRO, WsiBuffer.DTYPE_NZ, WsiBuffer.DTYPE_P]:
            self.put_byte(scale)  # scale
            self.put_byte(size & 0x00ff)  # digits / precision
        else:
            self.put_short(0)  # unused scale & precision

        self.put_short(0)  # reserved field, unused

        # point to the value location on the way out...
        self.m_cur_pos = save_cur_pos

    def get_param_header(self, phidx: int):
        WsiUtils.check_type(phidx, int)
        self.m_param_header = phidx
        self.m_cur_param_idx = 0

    def get_param_entry(self) -> int:
        self.m_cur_param_idx += 1
        return self.get_param_entry_phindex_paramcnt(self.m_param_header, self.m_cur_param_idx)

    def get_param_entry_phindex_paramcnt(self, phindex: int, paramcnt: int) -> int:
        WsiUtils.check_type(phindex, int)
        WsiUtils.check_type(paramcnt, int)
        self.m_param_header = phindex
        self.m_cur_param_idx = paramcnt
        # We could make this method take a datatype and validate
        # it against the parameter entry coming in from the server???
        val_size = int(self.get_short_d_type_new_pos(WsiBuffer.DTYPE_W, phindex + ((paramcnt - 1) * 12)))
        # Change it from a signed to an unsigned length...
        if val_size < 0:
            val_size = 65536 + val_size
        val_type = int(self.get_byte_d_type_new_pos(WsiBuffer.DTYPE_B, phindex + ((paramcnt - 1) * 12) + 2))
        val_class = int(self.get_byte_d_type_new_pos(WsiBuffer.DTYPE_B, phindex + ((paramcnt - 1) * 12) + 3))
        v_offset = self.get_int_d_type_new_pos(WsiBuffer.DTYPE_L, phindex + ((paramcnt - 1) * 12) + 4)
        # point to the value on the way out...
        self.m_cur_pos = v_offset
        # If this is an array, return the number of elements
        if ((val_class == 4) or (val_class == 10)) and ((val_type == 2) or (val_type == 6)):
            m_ary_hdr_idx = self.m_cur_pos
            ary_size = self.get_int_d_type_new_pos(WsiBuffer.DTYPE_L, m_ary_hdr_idx + 12)
            val_size = ary_size
            self.m_cur_pos = v_offset
        return val_size

    """
    /*
     * putArrayHeader inserts an Array header into the Stream buffer.
     *    The built header has the exact same layout as the fixed portion
     *    of an Array Descriptor on OpenVMS.
     */
    """

    def put_array_header(self, d_type: int, d_class: int, size: int, scale: int, dims: int, row_col: bool) -> int:
        WsiUtils.check_type(d_type, int)
        WsiUtils.check_type(d_class, int)
        WsiUtils.check_type(size, int)
        WsiUtils.check_type(scale, int)
        WsiUtils.check_type(dims, int)
        WsiUtils.check_type(row_col, bool)

        ary_idx = self.m_cur_pos
        self.ensure_space(24 + (dims * 12))  # Ensure space for Array DX
        if d_type == WsiBuffer.DTYPE_T and size == 0:
            self.put_short(8)  # length
            self.put_byte(WsiBuffer.DTYPE_DSC)  # Assume Dynamic String Array
        else:
            self.put_short(size & 0xffff)  # length
            self.put_byte(d_type)  # data type

        self.put_byte(d_class)  # class type
        self.put_int(0)  # Pointer

        self.put_byte(scale)  # scale
        self.put_byte(0)  # /digits/precision - should be 0?

        a_flags = 64  # Set "don't deallocate" flag
        if d_class == WsiBuffer.CLASS_A:
            a_flags = 192  # Set multiplier & Bounds block flags
            if row_col is False:
                a_flags += 32  # Set Column/Row flag

        self.put_byte_d_type(a_flags, WsiBuffer.DTYPE_B)  # Array flags
        self.put_byte_d_type(dims, WsiBuffer.DTYPE_B)  # dim count

        self.put_int(0)  # Array size
        self.put_int(0)  # A0

        for i in range(0, dims):
            self.put_int(0)  # Multiplier/Stride n
            self.put_int(0)  # Lower n
            self.put_int(0)  # Upper n

        self.align_to(16)
        value_idx = self.m_cur_pos
        self.put_int_d_type_new_pos(value_idx, WsiBuffer.DTYPE_L, ary_idx + 4)  # pointer field
        self.put_int_d_type_new_pos(value_idx, WsiBuffer.DTYPE_L, ary_idx + 16)  # A0 field
        self.m_ary_hdr_idx = ary_idx
        self.m_cur_dsc_pos = value_idx
        self.m_cur_pos = value_idx
        return ary_idx

    """
    /*
     *    putArrayDim inserts Dimension information into the Stream buffer.
     *    It takes an Array Handle, a dimension number, and lower & upper
     *    bounds for the dimension
     */
    """

    def put_array_dim(self, dim_cnt: int, d_lower: int, d_upper: int):
        WsiUtils.check_type(dim_cnt, int)
        WsiUtils.check_type(d_lower, int)
        WsiUtils.check_type(d_upper, int)

        elem_size = self.get_short_d_type_new_pos(WsiBuffer.DTYPE_W, self.m_ary_hdr_idx)
        # Change it from a signed to an unsigned length...
        if elem_size < 0:
            elem_size = 65536 + elem_size
        d_type = self.get_byte_d_type_new_pos(WsiBuffer.DTYPE_B, self.m_ary_hdr_idx + 2)
        d_class = self.get_byte_d_type_new_pos(WsiBuffer.DTYPE_B, self.m_ary_hdr_idx + 3)
        dims = self.get_byte_d_type_new_pos(WsiBuffer.DTYPE_B, self.m_ary_hdr_idx + 11)

        if d_type == WsiBuffer.DTYPE_P:
            elem_size = elem_size / 2 + 1
        self.put_int_d_type_new_pos(d_lower, WsiBuffer.DTYPE_L, self.m_ary_hdr_idx + 20 + (dims * 4) + (dim_cnt - 1) * 8)
        self.put_int_d_type_new_pos(d_upper, WsiBuffer.DTYPE_L, self.m_ary_hdr_idx + 20 + (dims * 4) + (dim_cnt - 1) * 8 + 4)

        # Compute the Stride / Multiplier factor for this dimension
        multi_value = 0
        if d_class == WsiBuffer.CLASS_A:
            multi_value = (d_upper - d_lower) + 1
        else:
            if dim_cnt == dims:
                multi_value = elem_size
            else:
                # Compute the Stride / Multiplier factor for this dimension
                ds = self.get_int_d_type_new_pos(WsiBuffer.DTYPE_L, self.m_ary_hdr_idx + 20 + dim_cnt * 4)
                dl = self.get_int_d_type_new_pos(WsiBuffer.DTYPE_L, self.m_ary_hdr_idx + 20 + dims * 4 + dim_cnt * 8)
                du = self.get_int_d_type_new_pos(WsiBuffer.DTYPE_L, self.m_ary_hdr_idx + 20 + dims * 4 + dim_cnt * 8 + 4)
                multi_value = ((du - dl) + 1) * ds
        self.put_int_d_type_new_pos(multi_value, WsiBuffer.DTYPE_L, self.m_ary_hdr_idx + 20 + (dim_cnt - 1) * 4)
        #  If this is the last dimension to be added, compute Array size
        if dim_cnt == 1:
            ary_size = elem_size
            dl = 0
            du = 0
            for i in range(0, dims):
                dl = self.get_int_d_type_new_pos(WsiBuffer.DTYPE_L, self.m_ary_hdr_idx + 20 + dims * 4 + i * 8)
                du = self.get_int_d_type_new_pos(WsiBuffer.DTYPE_L, self.m_ary_hdr_idx + 20 + dims * 4 + (i * 8 + 4))
                ary_size = (du - dl + 1) * ary_size
            self.put_int_d_type_new_pos(ary_size, WsiBuffer.DTYPE_L, self.m_ary_hdr_idx + 12)
            if d_type == WsiBuffer.DTYPE_DSC:
                self.m_cur_pos = self.m_cur_dsc_pos + ary_size  # Dynamic String Array
            else:
                self.m_cur_pos = self.m_cur_dsc_pos
            # Do final set up of value area
            self.ensure_space(ary_size)
        else:
            self.m_cur_pos = self.m_cur_dsc_pos

    """
    /*
    * getArrayHeader
    *   This routine is called to skip the Array header within the buffer
    */
    """

    def get_array_header(self) -> int:
        self.m_ary_hdr_idx = self.m_cur_pos
        d_type = self.get_byte_d_type_new_pos(WsiBuffer.DTYPE_B, self.m_ary_hdr_idx + 2)
        dims = self.get_byte_d_type_new_pos(WsiBuffer.DTYPE_B, self.m_ary_hdr_idx + 11)
        ary_size = self.get_int_d_type_new_pos(WsiBuffer.DTYPE_L, self.m_ary_hdr_idx + 12)
        self.m_cur_dsc_pos = self.get_int_d_type_new_pos(WsiBuffer.DTYPE_L, self.m_ary_hdr_idx + 4)
        if d_type == WsiBuffer.DTYPE_DSC:
            self.m_cur_pos = self.m_cur_dsc_pos + ary_size
        else:
            self.m_cur_pos = self.m_cur_dsc_pos
        return self.m_cur_pos

    """
    /*
    *    putFixupEntry inserts a structure fixup entry into the Stream buffer.
    *    The built header has the exact same layout as a Scaled Decimal
    *    Descriptor on OpenVMS.
    */
    """

    def put_fixup_entry(self, d_type: int, offset: int, elements: int):
        WsiUtils.check_type(d_type, int)
        WsiUtils.check_type(offset, int)
        WsiUtils.check_type(elements, int)

        self.ensure_space(8)  # Ensure space for entry
        self.put_int(elements)  # 1 if primitive, # of elements if array
        self.put_short(offset & 0xFFFF)  # Offset of field to be fixed up
        self.put_byte(d_type & 0xFF)  # OpenVMS Datatype to be converted to
        self.put_byte(0)  # <reserved for later>

    """
    /*
    * setAlignment inserts padding as needed to force the next entry to be
    *    at a specific alignment within the buffer.
    */
    """

    def align_to(self, alignment: int):
        WsiUtils.check_type(alignment, int)
        a_mask = alignment - 1
        # Return if we have the correct alignment already
        if self.m_cur_pos & a_mask == 0:
            return
        self.ensure_space(alignment)  # Ensure space for alignment padding
        self.m_cur_pos = (int(self.m_cur_pos / alignment) * alignment) + alignment

    """
    /**
     *  Copy another WsiBuffer into this output stream.
     *      Optimized to not create an extra object
     *
     *  @param  v       WsiBuffer to insert.
     *  @param size     # bytes to copy from other WsiBuffer
     */
    """

    def put_wsi_buffer_size(self, in_buffer: 'WsiBuffer', size: int):
        WsiUtils.check_type(in_buffer, WsiBuffer)
        WsiUtils.check_type(size, int)
        in_ary = in_buffer.get_buffer_internal()
        in_base = in_buffer.get_base()
        self.ensure_space(size)
        self.m_buffer[self.m_cur_pos:self.m_cur_pos + size] = in_ary[in_base:in_base + size]
        self.m_cur_pos += size

    def put_wsi_buffer_size_new_pos(self, in_buffer: 'WsiBuffer', size: int, new_pos: int):
        self.set_position(new_pos)
        self.put_wsi_buffer_size(in_buffer, size)

    """
    /**
    * Place a boolean value into the output stream.
    *
    *  @param v        boolean value to record
    *  @param dtype    native VMS data type
    */
    """

    def put_bool_d_type(self, value: bool, d_type: int):
        WsiUtils.check_type(value, bool)
        WsiUtils.check_type(d_type, int)
        self.ensure_space(1)
        self.m_buffer[self.m_cur_pos] = 1 if value else 0
        self.m_cur_pos += 1

    def put_bool_d_type_new_pos(self, value: bool, d_type: int, new_pos: int):
        self.set_position(new_pos)
        self.put_bool_d_type(value, d_type)

    """
    /**
    *  Place a byte value into the output stream.
    *
    *  @param  v   byte value to record.
    *  @param dtype    native VMS data type
    */
    """

    def put_byte(self, value: int):
        WsiUtils.check_value_interval(value, IntegerTypes.EXT_BYTE)
        self.ensure_space(1)
        self.m_buffer[self.m_cur_pos] = value
        self.m_cur_pos += 1

    def put_byte_d_type(self, value: int, d_type: int):
        WsiUtils.check_value_interval(value, IntegerTypes.EXT_BYTE)
        WsiUtils.check_type(d_type, int)
        self.ensure_space(1)
        self.m_buffer[self.m_cur_pos] = value
        self.m_cur_pos += 1

    def put_byte_d_type_new_pos(self, value: int, d_type: int, new_pos: int):
        self.set_position(new_pos)
        self.put_byte_d_type(value, d_type)

    """
    /**
    *  Place a short (16-bit) value into the output stream.
    *
    *  @param  v   short integer value to record.
    *  @param dtype    native VMS data type
    */
    """

    def put_short(self, value: int):
        WsiUtils.check_value_interval(value, IntegerTypes.SHORT)
        self.ensure_space(2)
        self.m_buffer[self.m_cur_pos] = value & 0x0ff
        self.m_cur_pos += 1
        self.m_buffer[self.m_cur_pos] = (value >> WsiBuffer.__BYTE_BITS) & 0x0ff
        self.m_cur_pos += 1

    def put_short_d_type(self, value: int, d_type: int):
        WsiUtils.check_value_interval(value, IntegerTypes.SHORT)
        WsiUtils.check_type(d_type, int)
        self.ensure_space(2)
        self.m_buffer[self.m_cur_pos] = value & 0x0ff
        self.m_cur_pos += 1
        self.m_buffer[self.m_cur_pos] = (value >> WsiBuffer.__BYTE_BITS) & 0x0ff
        self.m_cur_pos += 1

    def put_short_d_type_new_pos(self, value: int, d_type: int, new_pos: int):
        self.set_position(new_pos)
        self.put_short_d_type(value, d_type)

    """
    /**
    *  Place a 32-bit integer value into the output stream.
    *
    *  @param  v   longword integer value to record.
    *  @param dtype    native VMS data type
    */
    """

    def put_int(self, value: int):
        WsiUtils.check_value_interval(value, IntegerTypes.INT)
        self.ensure_space(4)
        self.m_buffer[self.m_cur_pos] = value & 0x0ff
        self.m_cur_pos += 1
        self.m_buffer[self.m_cur_pos] = (value >> WsiBuffer.__BYTE_BITS) & 0x0ff
        self.m_cur_pos += 1
        self.m_buffer[self.m_cur_pos] = (value >> (WsiBuffer.__BYTE_BITS * 2)) & 0x0ff
        self.m_cur_pos += 1
        self.m_buffer[self.m_cur_pos] = (value >> (WsiBuffer.__BYTE_BITS * 3)) & 0x0ff
        self.m_cur_pos += 1

    def put_int_d_type(self, value: int, d_type: int):
        WsiUtils.check_value_interval(value, IntegerTypes.INT)
        WsiUtils.check_type(d_type, int)
        self.ensure_space(4)
        self.m_buffer[self.m_cur_pos] = value & 0x0ff
        self.m_cur_pos += 1
        self.m_buffer[self.m_cur_pos] = (value >> WsiBuffer.__BYTE_BITS) & 0x0ff
        self.m_cur_pos += 1
        self.m_buffer[self.m_cur_pos] = (value >> (WsiBuffer.__BYTE_BITS * 2)) & 0x0ff
        self.m_cur_pos += 1
        self.m_buffer[self.m_cur_pos] = (value >> (WsiBuffer.__BYTE_BITS * 3)) & 0x0ff
        self.m_cur_pos += 1

    def put_int_d_type_new_pos(self, value: int, d_type: int, new_pos: int):
        self.set_position(new_pos)
        self.put_int_d_type(value, d_type)

    """
    /**
    *  Place a long int (64-bit) value into the output stream.
    *
    *  @param  v   quadword integer value to record.
    *  @param dtype    native VMS data type
    */
    """

    def put_long_d_type(self, value: int, d_type: int):
        WsiUtils.check_value_interval(value, IntegerTypes.LONG)
        WsiUtils.check_type(d_type, int)
        start_pos = self.m_cur_pos
        self.ensure_space(8)
        self.m_buffer[self.m_cur_pos] = value & 0x0ff
        self.m_cur_pos += 1
        self.m_buffer[self.m_cur_pos] = (value >> WsiBuffer.__BYTE_BITS) & 0x0ff
        self.m_cur_pos += 1
        self.m_buffer[self.m_cur_pos] = (value >> (WsiBuffer.__BYTE_BITS * 2)) & 0x0ff
        self.m_cur_pos += 1
        self.m_buffer[self.m_cur_pos] = (value >> (WsiBuffer.__BYTE_BITS * 3)) & 0x0ff
        self.m_cur_pos += 1
        self.m_buffer[self.m_cur_pos] = (value >> (WsiBuffer.__BYTE_BITS * 4)) & 0x0ff
        self.m_cur_pos += 1
        self.m_buffer[self.m_cur_pos] = (value >> (WsiBuffer.__BYTE_BITS * 5)) & 0x0ff
        self.m_cur_pos += 1
        self.m_buffer[self.m_cur_pos] = (value >> (WsiBuffer.__BYTE_BITS * 6)) & 0x0ff
        self.m_cur_pos += 1
        self.m_buffer[self.m_cur_pos] = (value >> (WsiBuffer.__BYTE_BITS * 7)) & 0x0ff
        self.m_cur_pos += 1

        if d_type == WsiBuffer.DTYPE_O or d_type == WsiBuffer.DTYPE_OU:
            self.ensure_space(8)
            if d_type == WsiBuffer.DTYPE_O and value < 0:
                # This is a signed octaword type, so we have another quadword to sign extend...
                self.m_buffer[self.m_cur_pos] = - 1
                self.m_cur_pos += 1
                self.m_buffer[self.m_cur_pos] = - 1
                self.m_cur_pos += 1
                self.m_buffer[self.m_cur_pos] = - 1
                self.m_cur_pos += 1
                self.m_buffer[self.m_cur_pos] = - 1
                self.m_cur_pos += 1
                self.m_buffer[self.m_cur_pos] = - 1
                self.m_cur_pos += 1
                self.m_buffer[self.m_cur_pos] = - 1
                self.m_cur_pos += 1
                self.m_buffer[self.m_cur_pos] = - 1
                self.m_cur_pos += 1
                self.m_buffer[self.m_cur_pos] = - 1
                self.m_cur_pos += 1
            else:
                # This is an octaword type, so we have another quadword to zero out.
                self.m_buffer[self.m_cur_pos] = 0
                self.m_cur_pos += 1
                self.m_buffer[self.m_cur_pos] = 0
                self.m_cur_pos += 1
                self.m_buffer[self.m_cur_pos] = 0
                self.m_cur_pos += 1
                self.m_buffer[self.m_cur_pos] = 0
                self.m_cur_pos += 1
                self.m_buffer[self.m_cur_pos] = 0
                self.m_cur_pos += 1
                self.m_buffer[self.m_cur_pos] = 0
                self.m_cur_pos += 1
                self.m_buffer[self.m_cur_pos] = 0
                self.m_cur_pos += 1
                self.m_buffer[self.m_cur_pos] = 0
                self.m_cur_pos += 1
        for i in range(start_pos, self.m_cur_pos):
            if self.m_buffer[i] != 0:
                self.m_buffer[i] = WsiUtils.int_to_byte(self.m_buffer[i])

    def put_long_d_type_new_pos(self, value: int, d_type: int, new_pos: int):
        self.set_position(new_pos)
        self.put_long_d_type(value, d_type)

    """
    /**
    *  Place a IEEE short (32-bit) float into the output stream.
    *
    *  @param  f       float value to record.
    *  @param  dtype   destination data type (not used)
    */
    """

    def put_float_d_type(self, f_value: numpy.float32, d_type: int):
        WsiUtils.check_type(f_value, numpy.float32)
        WsiUtils.check_type(d_type, int)
        start_pos = self.m_cur_pos
        value = WsiUtils.float_to_raw_int_bits(f_value)
        self.ensure_space(4)
        self.m_buffer[self.m_cur_pos] = value & 0x0ff
        self.m_cur_pos += 1
        self.m_buffer[self.m_cur_pos] = (value >> WsiBuffer.__BYTE_BITS) & 0x0ff
        self.m_cur_pos += 1
        self.m_buffer[self.m_cur_pos] = (value >> (WsiBuffer.__BYTE_BITS * 2)) & 0x0ff
        self.m_cur_pos += 1
        self.m_buffer[self.m_cur_pos] = (value >> (WsiBuffer.__BYTE_BITS * 3)) & 0x0ff
        self.m_cur_pos += 1
        for i in range(start_pos, self.m_cur_pos):
            if self.m_buffer[i] != 0:
                self.m_buffer[i] = WsiUtils.int_to_byte(self.m_buffer[i])

    def put_float_d_type_new_pos(self, f_value: numpy.float32, d_type: int, new_pos: int):
        self.set_position(new_pos)
        self.put_float_d_type(f_value, d_type)

    """
    /**
    *  Place a IEEE long (64-bit) float into the output stream.
    *
    *  @param  f       float value to record.
    *  @param  dtype   destination data type (used to determine if space
    *                  is needed for an extended IEEE float)
    */
    """

    def put_double_d_type(self, f_value: float, d_type: int):
        WsiUtils.check_type(f_value, float)
        WsiUtils.check_type(d_type, int)
        value = WsiUtils.double_to_raw_int_bits(f_value)
        self.ensure_space(8)
        self.m_buffer[self.m_cur_pos] = value & 0x0ff
        self.m_cur_pos += 1
        self.m_buffer[self.m_cur_pos] = (value >> WsiBuffer.__BYTE_BITS) & 0x0ff
        self.m_cur_pos += 1
        self.m_buffer[self.m_cur_pos] = (value >> (WsiBuffer.__BYTE_BITS * 2)) & 0x0ff
        self.m_cur_pos += 1
        self.m_buffer[self.m_cur_pos] = (value >> (WsiBuffer.__BYTE_BITS * 3)) & 0x0ff
        self.m_cur_pos += 1
        self.m_buffer[self.m_cur_pos] = (value >> (WsiBuffer.__BYTE_BITS * 4)) & 0x0ff
        self.m_cur_pos += 1
        self.m_buffer[self.m_cur_pos] = (value >> (WsiBuffer.__BYTE_BITS * 5)) & 0x0ff
        self.m_cur_pos += 1
        self.m_buffer[self.m_cur_pos] = (value >> (WsiBuffer.__BYTE_BITS * 6)) & 0x0ff
        self.m_cur_pos += 1
        self.m_buffer[self.m_cur_pos] = (value >> (WsiBuffer.__BYTE_BITS * 7)) & 0x0ff
        self.m_cur_pos += 1
        if d_type == WsiBuffer.DTYPE_FX:
            # It's an extended precision value, so we need to zero the next quadword.
            self.ensure_space(8)
            self.m_buffer[self.m_cur_pos] = 0
            self.m_cur_pos += 1
            self.m_buffer[self.m_cur_pos] = 0
            self.m_cur_pos += 1
            self.m_buffer[self.m_cur_pos] = 0
            self.m_cur_pos += 1
            self.m_buffer[self.m_cur_pos] = 0
            self.m_cur_pos += 1
            self.m_buffer[self.m_cur_pos] = 0
            self.m_cur_pos += 1
            self.m_buffer[self.m_cur_pos] = 0
            self.m_cur_pos += 1
            self.m_buffer[self.m_cur_pos] = 0
            self.m_cur_pos += 1
            self.m_buffer[self.m_cur_pos] = 0
            self.m_cur_pos += 1

    def put_double_d_type_new_pos(self, f_value: float, d_type: int, new_pos: int):
        self.set_position(new_pos)
        self.put_double_d_type(f_value, d_type)

    """
    /**
     *  Single character to record into the output stream, converting from
     *  two byte representation to localized 8-bit form.
     *
     *  @param  v       character to insert.
     *  @param dtype    destination data type (not used)
     */
    """

    def put_char_d_type(self, value: str, d_type: int):
        WsiUtils.check_type(value, str)
        if value.__len__() > 1:
            raise TypeError("value must be one symbol string")
        WsiUtils.check_type(d_type, int)
        self.ensure_space(1)
        self.m_buffer[self.m_cur_pos] = ord(value)
        self.m_cur_pos += 1

    def put_char_d_type_new_pos(self, value: str, d_type: int, new_pos: int):
        self.set_position(new_pos)
        self.put_char_d_type(value, d_type)

    """
    /**
     *  Place a String into the output stream.
     *   Depending on dtype, it will be placed in Static String or
     *   Variant String format.
     *  @param sobject  String to insert.
     *  @param len      for fixed strings, # of chars of string
     *  @param dtype    destination data type
     */
    """

    def put_str_null_term(self, value: str, null_term: int):
        self.put_str_d_type_len_null_term(value, WsiBuffer.DTYPE_T, 0, null_term)

    def put_str_d_type_null_term(self, value: str, d_type: int, null_term: int):
        self.put_str_d_type_len_null_term(value, d_type, 0, null_term)

    def put_str_d_type_len_null_term(self, s_object: str, d_type: int, len: int, null_term: int):
        WsiUtils.check_type(s_object, str)
        WsiUtils.check_type(d_type, int)
        WsiUtils.check_type(len, int)
        WsiUtils.check_type(null_term, int)

        c_chars = 0
        byte_len = 0

        if s_object is not None and s_object.__len__() != 0:
            str_len = s_object.__len__()
            if len == 0 or str_len < len:
                c_chars = str_len
                t = [""]*str_len
                for i in range(str_len):
                    t[i] = ord(s_object[i])
            else:
                c_chars = len  # truncate if string longer than len
                t_chars = [*s_object]
                t_str = t_chars[:len]
                t = [""]*t_str.__len__()
                for i in range(t_str.__len__()):
                    t[i] = ord(t_str[i])
            byte_len = t.__len__()
            if d_type == WsiBuffer.DTYPE_VT:
                self.put_short(c_chars)

            if len == 0 or null_term == 1:
                self.ensure_space(byte_len + 1)
            else:
                self.ensure_space(byte_len)

            for i in range(0, byte_len):
                self.m_buffer[self.m_cur_pos] = t[i]
                self.m_cur_pos += 1

            #  Null terminate if specified Length was 0 (dynamic string)
            #  PJH- This only adds a single byte null terminator!!

            if len == 0:
                self.m_buffer[self.m_cur_pos] = 0
                self.m_cur_pos += 1

        else:
            if d_type == WsiBuffer.DTYPE_VT:
                self.put_short(0)

        """
        // Add padding to end of string if string shorter than len
        // or null terminate
        // PJH- This only adds a single byte per character padding
        // and null terminator, regardless of character set being used.
        """
        if c_chars < len:
            self.ensure_space(len - c_chars)
            for i in range(c_chars, len):
                if 1 == null_term:
                    self.m_buffer[self.m_cur_pos] = 0
                    self.m_cur_pos += 1
                else:
                    self.m_buffer[self.m_cur_pos] = 32
                    self.m_cur_pos += 1
        elif c_chars == len and 1 == null_term:
            self.m_cur_pos -= 1
            self.m_buffer[self.m_cur_pos] = 0
            self.m_cur_pos += 1

    def put_str_d_type_new_pos_len_null_term(self, value: str, d_type: int, new_pos: int, len: int,
                                             null_term: int):
        self.set_position(new_pos)
        self.put_str_d_type_len_null_term(value, d_type, len, null_term)

    """
    /**
     *  Place a Decimal Numeric into the output stream.
     *
     *  @param  v       character to insert.
     *  @param dtype    destination data type
     */
    """

    def put_wsi_decimal(self, obj: 'WsiDecimal'):
        WsiUtils.check_type(obj, WsiDecimal)
        self.put_byte_ary_d_type(obj.get_buffer(), obj.get_decimal_type())

    def put_wsi_decimal_d_type_len_scale(self, obj: 'WsiDecimal', d_type: int, len: int, scale: int):
        WsiUtils.check_type(obj, WsiDecimal)
        self.put_byte_ary_d_type(obj.get_buffer_from_precision_scale_dec_type(len, scale, d_type), d_type)

    def put_wsi_decimal_d_type_new_pos_len_scale(self, obj: 'WsiDecimal', d_type: int, new_pos: int, len: int,
                                                 scale: int):
        self.set_position(new_pos)
        self.put_wsi_decimal_d_type_len_scale(obj, d_type, len, scale)

    """
    /**
     *  Place a Big Decimal into the output stream.
     *
     *  @param  v       character to insert.
     *  @param dtype    destination data type
     */
    """

    def put_big_decimal_d_type_precision_scale(self, obj: BigDecimal, d_type: int, len: int, scale: int):
        WsiUtils.check_type(obj, BigDecimal)
        bwxd = WsiDecimal.init_from_bd_value_precision_scale_dectype(obj, len, scale, d_type)
        self.put_byte_ary_d_type(bwxd.get_buffer_from_precision_scale_dec_type(len, scale, d_type), d_type)

    def put_big_decimal_d_type_new_pos_precision_scale(self, obj: BigDecimal, d_type: int, new_pos: int, len: int,
                                                       scale: int):
        self.set_position(new_pos)
        self.put_big_decimal_d_type_precision_scale(obj, d_type, len, scale)

    """
    /**
     *  Place a Big Integer into the output stream.
     *
     *  @param  v       character to insert.
     *  @param dtype    destination data type
     */
    """

    def put_big_integer_d_type(self, obj: int, d_type: int):
        WsiUtils.check_type(obj, int)
        WsiUtils.check_type(d_type, int)
        av = WsiUtils.int_to_bytes(obj)
        av_size = av.__len__()
        if av_size > 16:
            raise Exception("CVT-E-OVERFLOW, Overflow detected during conversion")

        self.ensure_space(16)

        for i in range(av_size - 1, -1, -1):
            self.m_buffer[self.m_cur_pos] = av[i]
            self.m_cur_pos += 1

        for i in range(0, 16-av_size, 1):
            if av[0] < 0:
                self.m_buffer[self.m_cur_pos] = -1
                self.m_cur_pos += 1
            else:
                self.m_buffer[self.m_cur_pos] = 0
                self.m_cur_pos += 1

    def put_big_integer_d_type_new_pos(self, obj: int, d_type: int, new_pos: int):
        self.set_position(new_pos)
        self.put_big_integer_d_type(obj, d_type)

    """
        /**
     *  Place a Calendar into the output stream.
     *
     *  @param  v       character to insert.
     *  @param dtype    destination data type
     */
    """

    def put_calendar(self, c_obj: 'datetime'):
        WsiUtils.check_type(c_obj, datetime.datetime)
        qtime = int((c_obj - datetime.datetime(1970, 1, 1)).total_seconds())  # seconds till datetime(1, 1, 1)
        self.put_long_d_type(qtime, WsiBuffer.DTYPE_QU)

    def put_calendar_d_type(self, c_obj: 'datetime', d_type: int):
        WsiUtils.check_type(d_type, int)
        self.put_calendar(c_obj)

    def put_calendar_d_type_new_pos(self, c_obj: 'datetime', d_type: int, new_pos: int):
        self.set_position(new_pos)
        self.put_calendar_d_type(c_obj, d_type)

    """
    /**
     *  Place a Structure into the output stream.
     *
     *  @param  v       character to insert.
     *  @param dtype    destination data type
     */
    """

    def put_wsi_structure_d_type(self, s_obj: 'WsiStructure', d_type: int):
        WsiUtils.check_instance(s_obj, WsiStructure)
        WsiUtils.check_type(d_type, int)
        self.put_wsi_buffer_size(s_obj.wsi_buffer(), s_obj.length())

    def put_wsi_structure_d_type_new_pos(self, s_obj: 'WsiStructure', d_type: int, new_pos: int):
        self.set_position(new_pos)
        self.put_wsi_structure_d_type(s_obj, d_type)

    """
    /**
     *  Place a V2 Structure into the output stream.
     *
     *  @param  v       character to insert.
     *  @param dtype    destination data type
     */
    """

    def put_wsi_v2_structure_d_type(self, s_obj: 'WsiV2Structure', d_type: int):
        WsiUtils.check_instance(s_obj, WsiV2Structure)
        inner_struct = s_obj.retrieve_wsi_structure()
        self.put_wsi_structure_d_type(inner_struct, d_type)

    def put_wsi_v2_structure_d_type_new_pos(self, s_obj: 'WsiV2Structure', d_type: int, new_pos: int):
        self.set_position(new_pos)
        inner_struct = s_obj.retrieve_wsi_structure()
        self.put_wsi_structure_d_type(inner_struct, d_type)

    """
    /**
     *  Place an Array into the output stream.
     *
     *  @param  v       character to insert.
     *  @param dtype    destination data type
     */
    """

    def put_wsi_array(self, a_obj: 'WsiArray'):
        from wsit.main.com.vsi.wsi.wsi_array import WsiArray
        WsiUtils.check_type(a_obj, WsiArray)
        a_obj.export_array()

    def put_wsi_array_new_pos(self, a_obj: 'WsiArray', new_pos: int):
        self.set_position(new_pos)
        self.put_wsi_array(a_obj)

    """
    /**
     *  Place an Array into the output stream.
     *
     *  @param ary      Array to insert.
     *  @param dtype    destination data type
     */
    """

    def put_bool_ary_d_type(self, ary: List[bool], d_type: int):
        WsiUtils.check_list_type_of(ary, bool)
        l = ary.__len__()
        self.ensure_space(l)  # Faster if we can preallocate only once
        for i in range(l):
            self.put_bool_d_type(ary[i], d_type)

    def put_bool_ary_d_type_new_pos(self, ary: List[bool], d_type: int, new_pos: int):
        self.set_position(new_pos)
        self.put_bool_ary_d_type(ary, d_type)

    """
    /**
     *  Place an Array into the output stream.
     *
     *  @param ary      Array to insert.
     *  @param dtype    destination data type
     */
    """

    def put_byte_ary_d_type(self, ary: List[int], d_type: int):
        WsiUtils.check_list_type_of_intervals(ary, IntegerTypes.EXT_BYTE)
        WsiUtils.check_type(d_type, int)
        l = ary.__len__()
        self.ensure_space(l)  # Faster if we can preallocate only once
        #  Optimization in copying arrays of bytes
        self.m_buffer[self.m_cur_pos:self.m_cur_pos + l] = ary[:l]
        self.m_cur_pos += l

    def put_byte_ary_d_type_new_pos(self, ary: List[int], d_type: int, new_pos: int):
        self.set_position(new_pos)
        self.put_byte_ary_d_type(ary, d_type)

    """
    /**
     *  Place an Array into the output stream.
     *
     *  @param ary      Array to insert.
     *  @param dtype    destination data type
     */
    """

    def put_short_ary_d_type(self, ary: List[int], d_type: int):
        WsiUtils.check_list_type_of_intervals(ary, IntegerTypes.SHORT)
        l = ary.__len__()
        self.ensure_space(l)  # Faster if we can preallocate only once
        for i in range(l):
            self.put_short_d_type(ary[i], d_type)

    def put_short_ary_d_type_new_pos(self, ary: List[int], d_type: int, new_pos: int):
        self.set_position(new_pos)
        self.put_short_ary_d_type(ary, new_pos)

    """
    /**
     *  Place an Array into the output stream.
     *
     *  @param ary      Array to insert.
     *  @param dtype    destination data type
     */
    """

    def put_int_ary_d_type(self, ary: List[int], d_type: int):
        WsiUtils.check_list_type_of_intervals(ary, IntegerTypes.SHORT)
        l = ary.__len__()
        self.ensure_space(l * 4)  # Faster if we can preallocate only once
        for i in range(l):
            self.put_int_d_type(ary[i], d_type)

    def put_int_ary_d_type_new_pos(self, ary: List[int], d_type: int, new_pos: int):
        self.set_position(new_pos)
        self.put_int_ary_d_type(ary, d_type)

    """
    /**
     *  Place an Array into the output stream.
     *
     *  @param ary      Array to insert.
     *  @param dtype    destination data type
     */
    """

    def put_long_ary_d_type(self, ary: List[int], d_type: int):
        WsiUtils.check_list_type_of_intervals(ary, IntegerTypes.LONG)
        l = ary.__len__()
        self.ensure_space(l)  # Faster if we can preallocate only once
        for i in range(l):
            self.put_long_d_type(ary[i], d_type)

    def put_long_ary_d_type_new_pos(self, ary: List[int], d_type: int, new_pos: int):
        self.set_position(new_pos)
        self.put_long_ary_d_type(ary, d_type)

    """
    /**
     *  Place an Array into the output stream.
     *
     *  @param ary      Array to insert.
     *  @param dtype    destination data type
     */
    """

    def put_float_ary_d_type(self, ary: List[numpy.float32], d_type: int):
        WsiUtils.check_list_type_of(ary, numpy.float32)
        l = ary.__len__()
        self.ensure_space(l * 4)  # Faster if we can preallocate only once
        for i in range(l):
            self.put_float_d_type(ary[i], d_type)

    def put_float_ary_d_type_new_pos(self, ary: List[numpy.float32], d_type: int, new_pos: int):
        self.set_position(new_pos)
        self.put_float_ary_d_type(ary, d_type)

    """
     /**
     *  Place an Array into the output stream.
     *
     *  @param ary      Array to insert.
     *  @param dtype    destination data type
     */
    """

    def put_double_ary_d_type(self, ary: List[float], d_type: int):
        WsiUtils.check_list_type_of(ary, float)
        l = ary.__len__()
        self.ensure_space(l * 8)  # Faster if we can preallocate only once
        for i in range(l):
            self.put_double_d_type(ary[i], d_type)

    def put_double_ary_d_type_new_pos(self, ary: List[float], d_type: int, new_pos: int):
        self.set_position(new_pos)
        self.put_double_ary_d_type(ary, d_type)

    """
    /**
     *  Place an Array into the output stream.
     *
     *  @param ary      Array to insert.
     *  @param dtype    destination data type
     */
    """

    def put_str_ary_d_type_len_null_term(self, ary: List[str], d_type: int, len: int, null_term: int):
        WsiUtils.check_list_type_of(ary, str)
        WsiUtils.check_type(d_type, int)
        WsiUtils.check_type(len, int)
        WsiUtils.check_type(null_term, int)
        if d_type == WsiBuffer.DTYPE_T and len == 0:
            # assume Dynamic String is wanted...
            self.put_dyn_str_array_ary(ary)
        else:
            l = ary.__len__()
            self.ensure_space(l * len)  # Faster if we can preallocate only once
            for i in range(l):
                self.put_str_d_type_len_null_term(ary[i], d_type, len, null_term)

    def put_str_ary_d_type_new_pos_len_null_term(self, ary: List[str], d_type: int, new_pos: int, len: int,
                                                 null_term: int):
        self.set_position(new_pos)
        self.put_str_ary_d_type_len_null_term(ary, d_type, len, null_term)

    """
    /**
     *  Place an Array into the output stream.
     *
     *  @param ary      Array to insert.
     *  @param dtype    destination data type
     */
    """

    def put_wsi_structure_ary_d_type(self, ary: List['WsiStructure'], d_type: int):
        WsiUtils.check_list_type_of(ary, WsiStructure)
        l = ary.__len__()
        s_align = ary[0].alignment()
        self.ensure_space((l+1) * ary[0].length())  # Faster if we can preallocate only once

        for i in range(l):
            self.align_to(s_align)
            self.put_wsi_structure_d_type(ary[i], d_type)

    def put_wsi_structure_ary_d_type_new_pos(self, ary: List['WsiStructure'], d_type: int, new_pos: int):
        self.set_position(new_pos)
        self.put_wsi_structure_ary_d_type(ary, d_type)

    """
    /**
     *  Place a V2 Structure Array into the output stream.
     *
     *  @param ary      Array to insert.
     *  @param dtype    destination data type
     */
    """

    def put_wsi_v2_structure_ary_d_type(self, ary: List['WsiV2Structure'], d_type: int):
        WsiUtils.check_list_type_of(ary, WsiV2Structure)
        l = ary.__len__()
        inner_struct = ary[0].retrieve_wsi_structure()
        s_align = inner_struct.alignment()
        self.ensure_space((l + 1) * inner_struct.length())  # Faster if we can preallocate only once
        for i in range(l):
            self.align_to(s_align)
            inner_struct = ary[i].retrieve_wsi_structure()
            self.put_wsi_structure_d_type(inner_struct, d_type)

    def put_wsi_v2_structure_ary_d_type_new_pos(self, ary: List['WsiV2Structure'], d_type: int, new_pos: int):
        self.set_position(new_pos)
        self.put_wsi_v2_structure_ary_d_type(ary, d_type)

    """
    /**
     *  Place an Array into the output stream.
     *
     *  @param ary      Array to insert.
     *  @param dtype    destination data type
     */
    """

    def put_wsi_decimal_ary_d_type_len_scale(self, ary: List['WsiDecimal'], d_type: int, len: int, scale: int):
        WsiUtils.check_list_type_of(ary, WsiDecimal)
        l = ary.__len__()
        self.ensure_space(l * WsiDecimal.get_byte_count(len, d_type))
        for i in range(l):
            self.put_wsi_decimal_d_type_len_scale(ary[i], d_type, len, scale)

    def put_wsi_decimal_ary_d_type_new_pos_len_scale(self, ary: List['WsiDecimal'], d_type: int, new_pos: int, len: int,
                                                     scale: int):
        self.set_position(new_pos)
        self.put_wsi_decimal_ary_d_type_len_scale(ary, d_type, len, scale)

    """
    /**
         *  Place an Array into the output stream.
         *
         *  @param ary      Array to insert.
         *  @param dtype    destination data type
         */
    """

    def put_big_decimal_ary_d_type_len_scale(self, ary: List['BigDecimal'], d_type: int, len: int, scale: int):
        WsiUtils.check_list_type_of(ary, BigDecimal)
        l = ary.__len__()
        self.ensure_space(l * WsiDecimal.get_byte_count(len, d_type))  # Faster if we can preallocate only once
        for i in range(l):
            self.put_big_decimal_d_type_precision_scale(ary[i], d_type, len, scale)

    def put_big_decimal_ary_d_type_new_pos_len_scale(self, ary: List['BigDecimal'], d_type: int, new_pos: int, len: int,
                                                     scale: int):
        self.set_position(new_pos)
        self.put_big_decimal_ary_d_type_len_scale(ary, d_type, len, scale)

    """
    /**
     *  Place an Array into the output stream.
     *
     *  @param ary      Array to insert.
     *  @param dtype    destination data type
     */
    """

    def put_big_integer_ary_d_type(self, ary: List[int], d_type: int):
        WsiUtils.check_list_type_of_intervals(ary, IntegerTypes.INT)
        l = ary.__len__()
        self.ensure_space(l * 16)  # Faster if we can preallocate only once
        for i in range(l):
            self.put_big_integer_d_type(ary[i], d_type)

    def put_big_integer_ary_d_type_new_pos(self, ary: List[int], d_type: int, new_pos: int):
        self.set_position(new_pos)
        self.put_big_integer_ary_d_type(ary, d_type)

    """
    /**
     *  Place an Array into the output stream.
     *
     *  @param ary      Array to insert.
     *  @param dtype    destination data type
     */
     """
    def put_calendar_ary_d_type(self, ary: List['datetime'], d_type: int):
        WsiUtils.check_list_type_of(ary, datetime.datetime)
        l = ary.__len__()
        self.ensure_space(l*8)  # Faster if we can preallocate only once
        for i in range(l):
            self.put_calendar_d_type(ary[i], d_type)

    def put_calendar_ary_d_type_new_pos(self, ary: List['datetime'], d_type: int, new_pos: int):
        self.set_position(new_pos)
        self.put_calendar_ary_d_type(ary, d_type)
    """
    /*****************************************************************
    *
    * The following are extraction methods for the various entities that
    * can be extracted from a WsiBuffer.  These include headers, primitives,
    * padding, arrays, structures, and other WsiBuffers.
    *
    *****************************************************************/
    /**
     *  Retrieve a copy of a subset of the data buffer.
     *
     *  @return data buffer copy
     */
    """

    def get_buffer_len(self, len: int) -> List[int]:
        WsiUtils.check_type(len, int)
        if self.m_cur_pos + len > self.m_alloc_size:
            len = self.m_alloc_size - self.m_cur_pos
        temp_ary = self.m_buffer[self.m_cur_pos: self.m_cur_pos + len]
        self.m_cur_pos += len
        return temp_ary

    def get_buffer_start_pos_len(self, start_pos: int, len: int) -> List[int]:
        WsiUtils.check_type(start_pos, int)
        WsiUtils.check_type(len, int)
        temp_ary = []
        if start_pos < self.m_alloc_size:
            self.set_position(start_pos)
            if self.m_cur_pos + len > self.m_alloc_size:
                len = self.m_alloc_size - self.m_cur_pos
            temp_ary = self.m_buffer[self.m_cur_pos: self.m_cur_pos + len]
            self.m_cur_pos += len
        return temp_ary

    """
    /**
     *  Retrieve a single boolean item from the input stream.
     *
     * @return
     */
    """

    def get_bool_d_type(self, d_type: int) -> bool:
        WsiUtils.check_type(d_type, int)
        ret_val = False
        if self.m_buffer[self.m_cur_pos] > 0:
            ret_val = True
        self.m_cur_pos += 1
        return ret_val

    def get_bool_d_type_new_pos(self, d_type: int, new_pos: int) -> bool:
        self.set_position(new_pos)
        return self.get_bool_d_type(d_type)

    """
    /**
     * @return
     */
    """

    def get_byte(self) -> int:
        self.m_cur_pos += 1
        return self.m_buffer[self.m_cur_pos - 1]

    def get_byte_d_type(self, d_type: int) -> int:
        WsiUtils.check_type(d_type, int)
        self.m_cur_pos += 1
        return self.m_buffer[self.m_cur_pos - 1]

    def get_byte_d_type_new_pos(self, d_type: int, new_pos: int) -> int:
        self.set_position(new_pos)
        return self.get_byte_d_type(d_type)

    """
    /**
     * @return
     */
    """

    def get_short(self) -> int:
        v = self.m_buffer[self.m_cur_pos] & 0x0ff
        self.m_cur_pos += 1
        v |= (self.m_buffer[self.m_cur_pos] & 0x0ff) << 8
        self.m_cur_pos += 1
        return v

    def get_short_d_type(self, d_type: int) -> int:
        WsiUtils.check_type(d_type, int)
        v = self.m_buffer[self.m_cur_pos] & 0x0ff
        self.m_cur_pos += 1
        v |= (self.m_buffer[self.m_cur_pos] & 0x0ff) << 8
        self.m_cur_pos += 1
        return v

    def get_short_d_type_new_pos(self, d_type: int, new_pos: int) -> int:
        self.set_position(new_pos)
        return self.get_short_d_type(d_type)

    """
    /**
     * @return
     */
    """

    def get_int(self) -> int:
        v = self.m_buffer[self.m_cur_pos] & 0x0ff
        self.m_cur_pos += 1
        v |= (self.m_buffer[self.m_cur_pos] & 0x0ff) << 8
        self.m_cur_pos += 1
        v |= (self.m_buffer[self.m_cur_pos] & 0x0ff) << 16
        self.m_cur_pos += 1
        v |= (self.m_buffer[self.m_cur_pos] & 0x0ff) << 24
        self.m_cur_pos += 1
        return v

    def get_int_d_type(self, d_type: int) -> int:
        WsiUtils.check_type(d_type, int)
        v = self.m_buffer[self.m_cur_pos] & 0x0ff
        self.m_cur_pos += 1
        v |= (self.m_buffer[self.m_cur_pos] & 0x0ff) << 8
        self.m_cur_pos += 1
        v |= (self.m_buffer[self.m_cur_pos] & 0x0ff) << 16
        self.m_cur_pos += 1
        v |= (self.m_buffer[self.m_cur_pos] & 0x0ff) << 24
        self.m_cur_pos += 1
        return v

    def get_int_d_type_new_pos(self, d_type: int, new_pos: int) -> int:
        self.set_position(new_pos)
        return self.get_int_d_type(d_type)

    """
    /**
     * @return
     */
    """

    def get_long_d_type(self, d_type: int) -> int:
        WsiUtils.check_type(d_type, int)
        v = self.m_buffer[self.m_cur_pos] & 0x0ff
        self.m_cur_pos += 1
        v |= (self.m_buffer[self.m_cur_pos] & 0x0ff) << 8
        self.m_cur_pos += 1
        v |= (self.m_buffer[self.m_cur_pos] & 0x0ff) << 16
        self.m_cur_pos += 1
        v |= (self.m_buffer[self.m_cur_pos] & 0x0ff) << 24
        self.m_cur_pos += 1
        v |= (self.m_buffer[self.m_cur_pos] & 0x0ff) << 32
        self.m_cur_pos += 1
        v |= (self.m_buffer[self.m_cur_pos] & 0x0ff) << 40
        self.m_cur_pos += 1
        v |= (self.m_buffer[self.m_cur_pos] & 0x0ff) << 48
        self.m_cur_pos += 1
        v |= (self.m_buffer[self.m_cur_pos] & 0x0ff) << 56
        self.m_cur_pos += 1
        if d_type == WsiBuffer.DTYPE_O or d_type == WsiBuffer.DTYPE_OU:
            v2 = self.m_buffer[self.m_cur_pos] & 0x0ff
            self.m_cur_pos += 1
            v2 |= (self.m_buffer[self.m_cur_pos] & 0x0ff) << 8
            self.m_cur_pos += 1
            v2 |= (self.m_buffer[self.m_cur_pos] & 0x0ff) << 16
            self.m_cur_pos += 1
            v2 |= (self.m_buffer[self.m_cur_pos] & 0x0ff) << 24
            self.m_cur_pos += 1
            v2 |= (self.m_buffer[self.m_cur_pos] & 0x0ff) << 32
            self.m_cur_pos += 1
            v2 |= (self.m_buffer[self.m_cur_pos] & 0x0ff) << 40
            self.m_cur_pos += 1
            v2 |= (self.m_buffer[self.m_cur_pos] & 0x0ff) << 48
            self.m_cur_pos += 1
            v2 |= (self.m_buffer[self.m_cur_pos] & 0x0ff) << 56
            self.m_cur_pos += 1
            if ((v2 == 0 or v2 == -1) and d_type == WsiBuffer.DTYPE_O) is False:
                raise Exception("CVT-E-OVERFLOW, Overflow detected during conversion")
        return v

    def get_long_d_type_new_pos(self, d_type: int, new_pos: int) -> int:
        self.set_position(new_pos)
        return self.get_long_d_type(d_type)

    """
    /**
     * @return
     */
    """

    def get_float_d_type(self, d_type: int) -> numpy.float32:
        WsiUtils.check_type(d_type, int)
        v = self.m_buffer[self.m_cur_pos] & 0x0ff
        self.m_cur_pos += 1
        v |= (self.m_buffer[self.m_cur_pos] & 0x0ff) << 8
        self.m_cur_pos += 1
        v |= (self.m_buffer[self.m_cur_pos] & 0x0ff) << 16
        self.m_cur_pos += 1
        v |= (self.m_buffer[self.m_cur_pos] & 0x0ff) << 24
        self.m_cur_pos += 1
        return WsiUtils.int_to_float(v)

    def get_float_d_type_new_pos(self, d_type: int, new_pos: int) -> numpy.float32:
        self.set_position(new_pos)
        return self.get_float_d_type(d_type)

    """
    /**
     * @return
     */
    """

    def get_double_d_type(self, d_type: int) -> float:
        WsiUtils.check_type(d_type, int)
        v = self.m_buffer[self.m_cur_pos] & 0x0ff
        self.m_cur_pos += 1
        v |= (self.m_buffer[self.m_cur_pos] & 0x0ff) << 8
        self.m_cur_pos += 1
        v |= (self.m_buffer[self.m_cur_pos] & 0x0ff) << 16
        self.m_cur_pos += 1
        v |= (self.m_buffer[self.m_cur_pos] & 0x0ff) << 24
        self.m_cur_pos += 1
        v |= (self.m_buffer[self.m_cur_pos] & 0x0ff) << 32
        self.m_cur_pos += 1
        v |= (self.m_buffer[self.m_cur_pos] & 0x0ff) << 40
        self.m_cur_pos += 1
        v |= (self.m_buffer[self.m_cur_pos] & 0x0ff) << 48
        self.m_cur_pos += 1
        v |= (self.m_buffer[self.m_cur_pos] & 0x0ff) << 56
        self.m_cur_pos += 1
        if d_type == WsiBuffer.DTYPE_FX or d_type == WsiBuffer.DTYPE_H:
            self.m_cur_pos += 8
        return WsiUtils.int_to_double(v)

    def get_double_d_type_new_pos(self, d_type: int, new_pos: int) -> float:
        self.set_position(new_pos)
        return self.get_double_d_type(d_type)

    """
    /**
     * @return
     */
    """

    def get_char(self) -> str:
        return ' '

    """
     /**
     * @return
     * @param len
     */
    """

    def get_str_len(self, len: int) -> str:
        WsiUtils.check_type(len, int)
        s = WsiUtils.bytes_to_string(self.m_buffer[self.m_cur_pos:self.m_cur_pos + len])
        self.m_cur_pos += len
        return s

    def get_str_d_type_len(self, d_type: int, len: int) -> str:
        WsiUtils.check_type(d_type, int)
        WsiUtils.check_type(len, int)
        if d_type == WsiBuffer.DTYPE_VT:
            actual_len = self.get_short()
            # Change it from a signed to an unsigned length...
            if actual_len < 0:
                actual_len = 65536 + actual_len
            s = WsiUtils.bytes_to_string(self.m_buffer[self.m_cur_pos:self.m_cur_pos + actual_len])
        else:
            s = WsiUtils.bytes_to_string(self.m_buffer[self.m_cur_pos:self.m_cur_pos + len])
        self.m_cur_pos += len
        return s

    def get_str_d_type_new_pos_len(self, d_type: int, new_pos: int, len: int) -> str:
        self.set_position(new_pos)
        return self.get_str_d_type_len(d_type, len)

    """
    /**
     *  We have a decimal string.
     *
     */
    """

    def get_decimal_d_type_precision_scale(self, d_type: int, precision: int, scale: int) -> 'WsiDecimal':
        byte_cnt = WsiDecimal.get_byte_count(precision, d_type)
        offset = self.m_cur_pos - self.__m_base

        d = WsiDecimal.init_from_buffer_offset_precision_scale_dec_type(self.get_buffer(), offset, precision, scale,
                                                                        d_type)
        self.m_cur_pos = self.__m_base + offset + byte_cnt
        return d

    def get_decimal_d_object(self, d_object: 'WsiDecimal') -> 'WsiDecimal':
        WsiUtils.check_type(d_object, WsiDecimal)
        d_type = d_object.get_decimal_type()
        precision = d_object.get_precision()
        scale = d_object.get_scale()
        return self.get_decimal_d_type_precision_scale(d_type, precision, scale)

    def get_decimal_d_type_new_pos_precision_scale(self, d_type: int, new_pos: int, precision: int,
                                                   scale: int) -> 'WsiDecimal':
        self.set_position(new_pos)
        return self.get_decimal_d_type_precision_scale(d_type, precision, scale)

    """
    /**
     *  We have a Big Decimal.
     *
     */
    """

    def get_big_decimal_d_type_precision_scale(self, d_type: int, precision: int, scale: int) -> 'BigDecimal':
        byte_cnt = WsiDecimal.get_byte_count(precision, d_type)
        offset = self.m_cur_pos - self.__m_base
        d = WsiDecimal.init_from_buffer_offset_precision_scale_dec_type(self.get_buffer(), offset, precision, scale, d_type)
        self.m_cur_pos = self.__m_base + offset + byte_cnt
        return d.get_value()

    """
    //    public BigDecimal getBigDecimal (BigDecimal dobject) throws Exception
//    {
//        int dtype = dobject.getDecimalType();
//        int precision = dobject.getPrecision();
//        int scale = dobject.scale();
//
//        return getBigDecimal (dtype, precision, scale);
//    }
    """

    def get_big_decimal_d_type_new_pos_precision_scale(self, d_type: int, new_pos: int, precision: int,
                                                       scale: int) -> 'BigDecimal':
        self.set_position(new_pos)
        return self.get_big_decimal_d_type_precision_scale(d_type, precision, scale)

    """
    /**
     *  We have a BigInteger.
     *
     */
    """

    def get_big_integer_d_type(self, d_type: int) -> int:
        WsiUtils.check_type(d_type, int)
        av = [0] * 16
        for i in range(15, -1, -1):
            av[i] = self.m_buffer[self.m_cur_pos]
            self.m_cur_pos += 1
        bigi = int.from_bytes(av, 'big')
        return bigi

    def get_big_integer_d_type_new_pos(self, d_type: int, new_pos: int) -> int:
        self.set_position(new_pos)
        return self.get_big_integer_d_type(d_type)

    """
    /**
    * @return
    */
    """
    def get_calendar(self) -> datetime:
        qtime = self.get_long_d_type(WsiBuffer.DTYPE_QU)
        return datetime.datetime.fromtimestamp(qtime)

    def get_calendar_d_type(self, d_type: int) -> datetime:
        WsiUtils.check_type(d_type, int)
        return self.get_calendar()

    def get_calendar_d_type_new_pos(self, d_type: int, new_pos: int) -> datetime:
        self.set_position(new_pos)
        return self.get_calendar_d_type(d_type)

    """
    /**
         *  We have a Structure.
         *
         */
    """

    def get_wsi_structure(self, s_object: WsiStructure):
        WsiUtils.check_instance(s_object, WsiStructure)
        # optimization...
        # Just point the structure's internal WsiBuffer into this byte array
        s_object.buffer_from_buffer_offset(self.m_buffer, self.m_cur_pos)
        self.m_cur_pos += s_object.length()

    def get_wsi_structure_new_pos(self, s_object: WsiStructure, new_pos: int):
        self.set_position(new_pos)
        self.get_wsi_structure(s_object)

    """
     /**
     *  We have a V2 Structure.
     *
     */
    """

    def get_v2_structure_s_object(self, s_object: 'WsiV2Structure'):
        WsiUtils.check_instance(s_object, WsiV2Structure)
        # optimization
        # Just point the structure's internal WsiBuffer into this byte array
        inner_struct = s_object.retrieve_wsi_structure()
        self.get_wsi_structure(inner_struct)

    def get_v2_structure_s_object_new_pos(self, s_object: 'WsiV2Structure', new_pos: int):
        self.set_position(new_pos)
        inner_struct = s_object.retrieve_wsi_structure()
        self.get_wsi_structure(inner_struct)

    """
    /**
     *  Return an Array from the stream.
     *
     *  @param dtype    destination data type
     */
    """

    def get_bool_array(self, d_type: int, elems: int) -> List[bool]:
        WsiUtils.check_type(elems, int)
        ret_ary = [False] * elems
        for i in range(elems):
            ret_ary[i] = self.get_bool_d_type(d_type)
        return ret_ary

    def get_bool_array_new_pos(self, d_type: int, elems: int, new_pos: int) -> List[bool]:
        self.set_position(new_pos)
        return self.get_bool_array(d_type, elems)

    """
    /**
     *  Return an Array from the stream.
     *
     *  @param dtype    destination data type
     */
    """

    def get_byte_array(self, d_type: int, elems: int) -> List[int]:
        WsiUtils.check_type(elems, int)
        ret_ary = [0] * elems
        for i in range(elems):
            ret_ary[i] = self.get_byte_d_type(d_type)
        return ret_ary

    def get_byte_array_new_pos(self, d_type: int, elems: int, new_pos: int) -> List[int]:
        self.set_position(new_pos)
        return self.get_byte_array(d_type, elems)

    """
    /**
     *  Return an Array from the stream.
     *
     *  @param dtype    destination data type
     */
    """

    def get_int_array(self, d_type: int, elems: int) -> List[int]:
        WsiUtils.check_type(elems, int)
        ret_ary = [0] * elems
        for i in range(elems):
            ret_ary[i] = self.get_int_d_type(d_type)
        return ret_ary

    def get_int_array_new_pos(self, d_type: int, elems: int, new_pos: int) -> List[int]:
        self.set_position(new_pos)
        return self.get_int_array(d_type, elems)

    """
    /**
     *  Return an Array from the stream.
     *
     *  @param dtype    destination data type
     */
    """

    def get_long_array(self, d_type: int, elems: int) -> List[int]:
        WsiUtils.check_type(elems, int)
        ret_ary = [0] * elems
        for i in range(elems):
            ret_ary[i] = self.get_long_d_type(d_type)
        return ret_ary

    def get_long_array_new_pos(self, d_type: int, elems: int, new_pos: int) -> List[int]:
        self.set_position(new_pos)
        return self.get_long_array(d_type, elems)

    """
        /**
     *  Return an Array from the stream.
     *
     *  @param dtype    destination data type
     */
    """

    def get_short_array(self, d_type: int, elems: int) -> List[int]:
        WsiUtils.check_type(elems, int)
        ret_ary = [0] * elems
        for i in range(elems):
            ret_ary[i] = self.get_short_d_type(d_type)
        return ret_ary

    def get_short_array_new_pos(self, d_type: int, elems: int, new_pos: int) -> List[int]:
        self.set_position(new_pos)
        return self.get_short_array(d_type, elems)

    """
    /**
     *  Return an Array from the stream.
     *
     *  @param dtype    destination data type
     */
    """

    def get_float_array(self, d_type: int, elems: int) -> List[numpy.float32]:
        WsiUtils.check_type(elems, int)
        ret_ary = [numpy.float32(0.0)] * elems
        for i in range(elems):
            ret_ary[i] = self.get_float_d_type(d_type)
        return ret_ary

    def get_float_array_new_pos(self, d_type: int, elems: int, new_pos: int) -> List[numpy.float32]:
        self.set_position(new_pos)
        return self.get_float_array(d_type, elems)

    """
    /**
     *  Return an Array from the stream.
     *
     *  @param dtype    destination data type
     */
    """

    def get_double_array(self, d_type: int, elems: int) -> List[float]:
        WsiUtils.check_type(elems, int)
        ret_ary = [0.0] * elems
        for i in range(elems):
            ret_ary[i] = self.get_double_d_type(d_type)
        return ret_ary

    def get_double_array_new_pos(self, d_type: int, elems: int, new_pos: int) -> List[float]:
        self.set_position(new_pos)
        return self.get_double_array(d_type, elems)

    """
    /**
     *  Return an Array from the stream.
     *
     *  @param dtype    destination data type
     */
    """

    def get_str_array(self, d_type: int, elems: int, len: int) -> List[str]:
        WsiUtils.check_type(d_type, int)
        WsiUtils.check_type(elems, int)
        WsiUtils.check_type(len, int)
        if d_type == WsiBuffer.DTYPE_T and len == 0:
            # assume Dynamic String is wanted...
            return self.get_dyn_str_array_elems(elems)
        ret_ary = [""] * elems
        for i in range(elems):
            ret_ary[i] = self.get_str_d_type_len(d_type, len)
        return ret_ary

    def get_str_array_new_pos(self, d_type: int, elems: int, new_pos: int, len: int) -> List[str]:
        self.set_position(new_pos)
        return self.get_str_array(d_type, elems, len)

    """
    /**
     *  Return an Array from the stream.
     *
     *  @param dtype    destination data type
     */
    """

    def get_decimal_array(self, d_type: int, elems: int, precision: int, scale: int) -> List['WsiDecimal']:
        WsiUtils.check_type(elems, int)
        ret_ary = [WsiDecimal()] * elems
        for i in range(elems):
            ret_ary[i] = self.get_decimal_d_type_precision_scale(d_type, precision, scale)
        return ret_ary

    def get_decimal_array_new_pos(self, d_type: int, elems: int, new_pos: int, precision: int, scale: int) -> List[WsiDecimal]:
        self.set_position(new_pos)
        return self.get_decimal_array(d_type, elems, precision, scale)

    """
    /**
     *  Return an Array from the stream.
     *
     *  @param dtype    destination data type
     */
    """

    def get_big_decimal_array(self, d_type: int, elems: int, precision: int, scale: int) -> List[BigDecimal]:
        WsiUtils.check_type(elems, int)
        ret_ary = [BigDecimal.init_from_str("0.0")] * elems
        for i in range(elems):
            ret_ary[i] = self.get_big_decimal_d_type_precision_scale(d_type, precision, scale)
        return ret_ary

    def get_big_decimal_array_new_pos(self, d_type: int, elems: int, new_pos: int, precision: int, scale: int) -> List[BigDecimal]:
        self.set_position(new_pos)
        return self.get_big_decimal_array(d_type, elems, precision, scale)

    """
    /**
     *  Return an Array from the stream.
     *
     *  @param dtype    destination data type
     */
    """

    def get_big_integer_array(self, d_type: int, elems: int) -> List[int]:
        WsiUtils.check_type(elems, int)
        ret_ary = [0] * elems
        for i in range(elems):
            ret_ary[i] = self.get_big_integer_d_type(d_type)
        return ret_ary

    def get_big_integer_array_new_pos(self, d_type: int, elems: int, new_pos: int) -> List[int]:
        self.set_position(new_pos)
        return self.get_big_integer_array(d_type, elems)

    """
    /**
     *  Return an Array from the stream.
     *
     *  @param dtype    destination data type
     */
     """
    def get_calendar_array(self, d_type: int, elems: int):
        WsiUtils.check_type(elems, int)
        ret_ary = [0]*elems
        for i in range(elems):
            ret_ary[i] = self.get_calendar_d_type(d_type)
        return ret_ary

    def get_calendar_array_new_pos(self, d_type: int, elems: int, new_pos: int):
        self.set_position(new_pos)
        return self.get_calendar_array(d_type, elems)

    """
    /**
     *  Place an Array into the output stream.
     *
     *  @param ary      Array to insert.
     *  @param dtype    destination data type
     */
    """

    def put_dyn_str_array_ary(self, ary: List[str]):
        WsiUtils.check_list_type_of(ary, str)
        l = ary.__len__()
        # This routine assumes that there has already been memory allocated
        # for the array of descriptors, pointed to by mCurDscPos.
        # The value part is pointed to by mCurPos
        for i in range(l):
            save_cur = self.m_cur_pos
            self.put_short_d_type_new_pos(len(ary[i]), WsiBuffer.DTYPE_W, self.m_cur_dsc_pos)  # length
            self.put_byte(WsiBuffer.DTYPE_T)  # data type
            self.put_byte(WsiBuffer.CLASS_D)  # class type
            self.put_int(save_cur)  # Address field
            self.m_cur_dsc_pos += 8
            self.put_str_d_type_len_null_term(ary[i], WsiBuffer.DTYPE_T, save_cur, 0)

    def put_dyn_str_array_ary_new_pos(self, ary: List[str], new_pos: int):
        self.set_position(new_pos)
        self.put_dyn_str_array_ary(ary)

    """
    /**
     *  Return an Array from the stream.
     *
     *  @param dtype    destination data type
     */
    """

    def get_dyn_str_array_elems(self, elems: int) -> List[str]:
        WsiUtils.check_type(elems, int)
        ret_ary = [""] * elems
        for i in range(elems):
            elem_size = self.get_short_d_type_new_pos(WsiBuffer.DTYPE_W, self.m_cur_dsc_pos)
            # Change it from a signed to an unsigned length...
            if elem_size < 0:
                elem_size = 65536 + elem_size
            aptr = self.get_int_d_type_new_pos(WsiBuffer.DTYPE_L, self.m_cur_dsc_pos + 4)
            self.m_cur_dsc_pos += 8
            ret_ary[i] = self.get_str_d_type_new_pos_len(WsiBuffer.DTYPE_T, aptr, elem_size)
        return ret_ary

    def get_dyn_str_array_elems_new_pos(self, elems: int, new_pos: int) -> List[str]:
        self.set_position(new_pos)
        return self.get_dyn_str_array_elems(elems)

    """
    /**
     *  Return a V1 Structure Array from the stream.
     *
     *  @param dtype    destination data type
     */
    """

    def get_wsi_structure_array_s_ary_elems(self, s_ary: List['WsiStructure'], elems: int):
        WsiUtils.check_list_type_of(s_ary, WsiStructure)
        WsiUtils.check_type(elems, int)
        s_align = s_ary[0].alignment()
        for i in range(elems):
            self.align_to(s_align)
            self.get_wsi_structure(s_ary[i])

    def get_wsi_structure_array_s_ary_elems_new_pos(self, s_ary: List['WsiStructure'], elems: int, new_pos: int):
        self.set_position(new_pos)
        self.get_wsi_structure_array_s_ary_elems(s_ary, elems)

    """
    /**
     *  Return a V2 Structure Array from the stream.
     *
     *  @param dtype    destination data type
     */
    """

    def get_v2_structure_array(self, s_ary: List['WsiV2Structure'], elems: int):
        WsiUtils.check_list_type_of(s_ary, WsiV2Structure)
        WsiUtils.check_type(elems, int)
        inner_struct = s_ary[0].retrieve_wsi_structure()
        s_align = inner_struct.alignment()
        for i in range(elems):
            self.align_to(s_align)
            inner_struct = s_ary[i].retrieve_wsi_structure()
            self.get_v2_structure_s_object(inner_struct)

    def get_v2_structure_array_new_pos(self, s_ary: List['WsiV2Structure'], elems: int, new_pos: int):
        self.set_position(new_pos)
        self.get_v2_structure_array(s_ary, elems)

    def __get_type_alignment(self, d_type: int) -> int:
        WsiUtils.check_type(d_type, int)
        ret_align = 1
        if d_type in [WsiBuffer.DTYPE_W, WsiBuffer.DTYPE_WU]:
            ret_align = 2
        elif d_type in [WsiBuffer.DTYPE_F, WsiBuffer.DTYPE_FS, WsiBuffer.DTYPE_L, WsiBuffer.DTYPE_LU]:
            ret_align = 4
        elif d_type in [WsiBuffer.DTYPE_D, WsiBuffer.DTYPE_G, WsiBuffer.DTYPE_FT, WsiBuffer.DTYPE_Q,
                        WsiBuffer.DTYPE_QU]:
            ret_align = 8
        elif d_type in [WsiBuffer.DTYPE_H, WsiBuffer.DTYPE_O, WsiBuffer.DTYPE_OU, WsiBuffer.DTYPE_STRUCT]:
            ret_align = 16
        return ret_align

    def to_string(self):
        ret_str = ""
        ret_str += "    WsiBuffer.mBuffer = " + str(self.m_buffer) + "\n"
        ret_str += "    WsiBuffer.mBase = " + str(self.__m_base) + "\n"
        ret_str += "    WsiBuffer.mAllocSize = " + str(self.m_alloc_size) + "\n"
        ret_str += "    WsiBuffer.mCurPos = " + str(self.m_cur_pos) + "\n"
        return ret_str
