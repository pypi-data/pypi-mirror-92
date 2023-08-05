from numpy import float32
from wsit.main.com.vsi.wsi.big_decimal import BigDecimal
from wsit.main.com.vsi.wsi.wsi_buffer import WsiBuffer
from wsit.main.com.vsi.wsi.wsi_decimal import WsiDecimal
from wsit.main.com.vsi.wsi.wsi_structure import WsiStructure
from wsit.main.com.vsi.wsi.wsi_utils import WsiUtils, IntegerTypes
from wsit.main.com.vsi.wsi.wsi_v2_structure import WsiV2Structure


class WsiArray:
    def __init__(self):
        self.m_value = None
        self.msgb = None
        self.d_type = 0
        self.d_class = 0
        self.size = 0
        self.scale = 0
        self.row_col = False
        self.largest = 0
        self.dim_ct = 0
        self.null_term = 0
        self.str_dims = ""
        self.dimensions = [0]
        self.by_ref = False
        self.wsi_array = False

    @classmethod
    def init_by_m_value(cls, m_value: 'object') -> 'WsiArray':
        WsiUtils.check_instance(m_value, object)
        wsi_array = cls()
        wsi_array.m_value = m_value
        return wsi_array

    @classmethod
    def init_by_all_vars(cls, m_value: 'object', msgb: 'WsiBuffer', d_type: int, d_class: int, size: int, scale: int,
                         row_col: bool, null_term: int, str_dims: str, by_ref: bool) -> 'WsiArray':
        WsiUtils.check_instance(m_value, object)
        from wsit.main.com.vsi.wsi.wsi_buffer import WsiBuffer
        WsiUtils.check_type(msgb, WsiBuffer)
        WsiUtils.check_type(d_type, int)
        WsiUtils.check_type(d_class, int)
        WsiUtils.check_type(size, int)
        WsiUtils.check_type(scale, int)
        WsiUtils.check_type(row_col, bool)
        WsiUtils.check_type(null_term, int)
        WsiUtils.check_type(str_dims, str)
        WsiUtils.check_type(by_ref, bool)
        wsi_array = cls()
        wsi_array.m_value = m_value
        wsi_array.msgb = msgb
        wsi_array.d_type = d_type
        wsi_array.d_class = d_class
        wsi_array.size = size
        wsi_array.scale = scale
        wsi_array.row_col = row_col
        wsi_array.null_term = null_term
        wsi_array.str_dims = str_dims
        wsi_array.by_ref = by_ref
        wsi_array.wsi_array = False
        wsi_array.bounds_check_array()
        return wsi_array

    @classmethod
    def init_by_all_vars_is_wsi_array(cls, m_value: 'object', msgb: 'WsiBuffer', d_type: int, d_class: int, size: int, scale: int,
                         row_col: bool, null_term: int, str_dims: str, by_ref: bool, is_wsi_array: bool) -> 'WsiArray':
        WsiUtils.check_instance(m_value, object)
        WsiUtils.check_type(msgb, WsiBuffer)
        WsiUtils.check_type(d_type, int)
        WsiUtils.check_type(d_class, int)
        WsiUtils.check_type(size, int)
        WsiUtils.check_type(scale, int)
        WsiUtils.check_type(row_col, bool)
        WsiUtils.check_type(null_term, int)
        WsiUtils.check_type(str_dims, str)
        WsiUtils.check_type(by_ref, bool)
        WsiUtils.check_type(is_wsi_array, bool)
        wsi_array = cls()
        wsi_array.m_value = m_value
        wsi_array.msgb = msgb
        wsi_array.d_type = d_type
        wsi_array.d_class = d_class
        wsi_array.size = size
        wsi_array.scale = scale
        wsi_array.row_col = row_col
        wsi_array.null_term = null_term
        wsi_array.str_dims = str_dims
        wsi_array.by_ref = by_ref
        wsi_array.wsi_array = is_wsi_array
        wsi_array.bounds_check_array()
        return wsi_array

    def get_value(self) -> object:
        return self.m_value

    def set_value(self, m_value: object):
        WsiUtils.check_instance(m_value, object)
        self.m_value = m_value

    """
    /**
     * Retrieves largest string within array for variable
     * length string arrays.
     */
    """

    def __get_largest_string(self, s: object):
        WsiUtils.check_instance(s, object)
        if WsiUtils.is_list_type_of(s, object) is True and WsiUtils.is_list_type_of(s, WsiStructure) is False\
                and WsiUtils.is_list_type_of(s, str) is False\
                and WsiUtils.is_list_type_of(s, WsiV2Structure) is False:
            # cast to last array level
            t = [0] * len(s)
            for i in range(len(s)):
                t[i] = object(s[i])
                self.__get_largest_string(t[i])
        else:
            # lowest level, check for varying string types
            for i in range(len(s)):
                tmp = str(s[i])
                if tmp is not None and len(tmp) > self.largest:
                    self.largest = len(tmp)

    """
    /**
     * Recursive algorithm2 used to exploit any sized array and place
     * values into buffer
     */
    """

    def __put_array_values(self, s: object):
        WsiUtils.check_instance(s, object)
        if WsiUtils.is_list_type_of(s, object) is True \
                and WsiUtils.is_list_type_of(s, WsiStructure) is False\
                and WsiUtils.is_list_type_of(s, str) is False\
                and WsiUtils.is_list_type_of(s, WsiV2Structure) is False\
                and WsiUtils.is_list_type_of(s, BigDecimal) is False\
                and WsiUtils.is_list_type_of(s, WsiDecimal) is False:
            # cast to lowest array level
            t = [0] * len(s)
            for i in range(len(s)):
                t[i] = object(s[i])
                self.__put_array_values(t[i])
        else:
            # lowest array level, single dimension
            t = [0] * len(s)
            if self.d_type in [WsiBuffer.DTYPE_F, WsiBuffer.DTYPE_FS]:
                for i in range(len(s)):
                    t[i] = float32(s[i])
                self.msgb.put_float_ary_d_type(t, self.d_type)
            elif self.d_type in [WsiBuffer.DTYPE_G, WsiBuffer.DTYPE_D, WsiBuffer.DTYPE_FT, WsiBuffer.DTYPE_FX]:
                for i in range(len(s)):
                    t[i] = float(s[i])
                self.msgb.put_double_ary_d_type(t, self.d_type)
            elif self.d_type in [WsiBuffer.DTYPE_BU, WsiBuffer.DTYPE_B]:
                for i in range(len(s)):
                    t[i] = int(s[i])
                WsiUtils.check_list_type_of_intervals(t, IntegerTypes.BYTE)
                self.msgb.put_byte_ary_d_type(t, self.d_type)
            elif self.d_type in [WsiBuffer.DTYPE_WU, WsiBuffer.DTYPE_W]:
                for i in range(len(s)):
                    t[i] = int(s[i])
                WsiUtils.check_list_type_of_intervals(t, IntegerTypes.SHORT)
                self.msgb.put_short_ary_d_type(t, self.d_type)
            elif self.d_type in [WsiBuffer.DTYPE_LU, WsiBuffer.DTYPE_L]:
                for i in range(len(s)):
                    t[i] = int(s[i])
                WsiUtils.check_list_type_of_intervals(t, IntegerTypes.INT)
                self.msgb.put_int_ary_d_type(t, self.d_type)
            elif self.d_type in [WsiBuffer.DTYPE_QU, WsiBuffer.DTYPE_Q, WsiBuffer.DTYPE_OU, WsiBuffer.DTYPE_O]:
                for i in range(len(s)):
                    t[i] = int(s[i])
                WsiUtils.check_list_type_of_intervals(t, IntegerTypes.LONG)
                self.msgb.put_long_ary_d_type(t, self.d_type)
            elif self.d_type in [WsiBuffer.DTYPE_V]:
                for i in range(len(s)):
                    t[i] = bool(s[i])
                WsiUtils.check_list_type_of(t, bool)
                self.msgb.put_bool_ary_d_type(t, self.d_type)
            elif self.d_type in [WsiBuffer.DTYPE_T, WsiBuffer.DTYPE_VT]:
                for i in range(len(s)):
                    t[i] = str(s[i])
                WsiUtils.check_list_type_of(t, str)
                self.msgb.put_str_ary_d_type_len_null_term(t, self.d_type, self.size, self.null_term)
            elif self.d_type in [WsiBuffer.DTYPE_STRUCT]:
                if WsiUtils.check_list_type_of(s, WsiV2Structure):
                    for i in range(len(s)):
                        t[i] = WsiV2Structure(s[i])
                    WsiUtils.check_list_type_of(t, WsiV2Structure)
                    self.msgb.put_wsi_v2_structure_ary_d_type(t, self.d_type)
                else:
                    for i in range(len(s)):
                        t[i] = WsiStructure(s[i])
                    WsiUtils.check_list_type_of(t, WsiStructure)
                    self.msgb.put_wsi_structure_ary_d_type(t, self.d_type)
            elif self.d_type in [WsiBuffer.DTYPE_NL, WsiBuffer.DTYPE_NR, WsiBuffer.DTYPE_P, WsiBuffer.DTYPE_NLO,
                                 WsiBuffer.DTYPE_NU, WsiBuffer.DTYPE_NRO, WsiBuffer.DTYPE_NZ]:
                if self.wsi_array is True:
                    for i in range(len(s)):
                        t[i] = BigDecimal(s[i])
                    WsiUtils.check_list_type_of(t, BigDecimal)
                    self.msgb.put_big_decimal_ary_d_type_len_scale(t, self.d_type, self.size, self.scale)
                else:
                    for i in range(len(s)):
                        t[i] = WsiDecimal(s[i])
                    WsiUtils.check_list_type_of(t, WsiDecimal)
                    self.msgb.put_wsi_decimal_ary_d_type_len_scale(t, self.d_type, self.size, self.scale)

    """
    /**
    * R2ecursive algorithm used to exploit any sized array and place
    * values into buffer
    */
    """

    def __get_array_values(self, s: object):
        WsiUtils.check_instance(s, object)
        if WsiUtils.is_list_type_of(s, object) is True\
                and WsiUtils.is_list_type_of(s, WsiStructure) is False\
                and WsiUtils.is_list_type_of(s, str) is False\
                and WsiUtils.is_list_type_of(s, WsiV2Structure) is False\
                and WsiUtils.is_list_type_of(s, BigDecimal) is False\
                and WsiUtils.is_list_type_of(s, WsiDecimal) is False:

            # cast to lowest array level
            t = [0] * len(s)
            for i in range(len(s)):
                t[i] = object(s[i])
                self.__get_array_values(t[i])
        else:
            # lowest array level, single dimension
            # x = [0]
            if self.d_type in [WsiBuffer.DTYPE_F, WsiBuffer.DTYPE_FS]:
                x = self.msgb.get_float_array(self.d_type, len(s))
                for i in range(len(x)):
                    s[i] = float32(x[i])
                return
            elif self.d_type in [WsiBuffer.DTYPE_G, WsiBuffer.DTYPE_D, WsiBuffer.DTYPE_FT, WsiBuffer.DTYPE_FX]:
                x = self.msgb.get_double_array(self.d_type, len(s))
                for i in range(len(x)):
                    s[i] = float(x[i])
                return
            elif self.d_type in [WsiBuffer.DTYPE_BU, WsiBuffer.DTYPE_B]:
                x = self.msgb.get_byte_array(self.d_type, len(s))
                for i in range(len(x)):
                    s[i] = int(x[i])
                WsiUtils.check_list_type_of_intervals(x, IntegerTypes.BYTE)
                return
            elif self.d_type in [WsiBuffer.DTYPE_WU, WsiBuffer.DTYPE_W]:
                x = self.msgb.get_short_array(self.d_type, len(s))
                for i in range(len(x)):
                    s[i] = int(x[i])
                WsiUtils.check_list_type_of_intervals(x, IntegerTypes.SHORT)
                return
            elif self.d_type in [WsiBuffer.DTYPE_LU, WsiBuffer.DTYPE_L]:
                x = self.msgb.get_int_array(self.d_type, len(s))
                for i in range(len(x)):
                    s[i] = int(x[i])
                WsiUtils.check_list_type_of_intervals(x, IntegerTypes.INT)
                return
            elif self.d_type in [WsiBuffer.DTYPE_QU, WsiBuffer.DTYPE_Q, WsiBuffer.DTYPE_OU, WsiBuffer.DTYPE_O]:
                x = self.msgb.get_long_array(self.d_type, len(s))
                for i in range(len(x)):
                    s[i] = int(x[i])
                WsiUtils.check_list_type_of_intervals(x, IntegerTypes.LONG)
                return
            elif self.d_type in [WsiBuffer.DTYPE_V]:
                x = self.msgb.get_bool_array(self.d_type, len(s))
                for i in range(len(x)):
                    s[i] = bool(x[i])
                WsiUtils.check_list_type_of(x, bool)
                return
            elif self.d_type in [WsiBuffer.DTYPE_T, WsiBuffer.DTYPE_VT]:
                x = self.msgb.get_str_array(self.d_type, len(s))
                for i in range(len(x)):
                    s[i] = object(x[i])
                WsiUtils.check_list_type_of(x, str)
                return
            elif self.d_type in [WsiBuffer.DTYPE_STRUCT]:
                x = [0]
                if WsiUtils.is_list_type_of(s, WsiV2Structure):
                    for i in range(len(s)):
                        s[i] = WsiV2Structure(x[i])
                    WsiUtils.check_list_type_of(x, WsiV2Structure)
                    self.msgb.get_v2_structure_array(x, len(s))
                else:
                    for i in range(len(s)):
                        s[i] = WsiStructure(x[i])
                    WsiUtils.check_list_type_of(x, WsiStructure)
                    self.msgb.get_wsi_structure_array_s_ary_elems(x, len(s))
            elif self.d_type in [WsiBuffer.DTYPE_NU, WsiBuffer.DTYPE_NL, WsiBuffer.DTYPE_NLO, WsiBuffer.DTYPE_NR,
                                 WsiBuffer.DTYPE_NRO, WsiBuffer.DTYPE_NZ, WsiBuffer.DTYPE_P]:
                if self.wsi_array is True:
                    x = self.msgb.get_big_decimal_array(self.d_type, len(s))
                    for i in range(len(x)):
                        s[i] = object(x[i])
                    WsiUtils.check_list_type_of(x, BigDecimal)
                    return
                else:
                    x = self.msgb.get_decimal_array(self.d_type, len(s))
                    for i in range(len(x)):
                        s[i] = object(x[i])
                    WsiUtils.check_list_type_of(x, WsiDecimal)
                    return

    """
    /**
     * setArrayDynamic
     *
     */
    """

    def __set_array_dimension(self, s: object):
        WsiUtils.check_instance(s, object)
        for i in range(self.dim_ct, 0, -1):
            self.msgb.put_array_dim(i, 0, len(s) - 1)
            s = s[0]

    """
    /**
     * Determines number of dimensions of the array object.
     */
    """

    def __set_dimension_count(self, s: object):
        WsiUtils.check_instance(s, object)
        name = s.__class__.__name__
        try:
            self.dim_ct = name.rindex('[') + 1
        except IndexError:
            self.dim_ct = 1

    """
    /**
    * exportArray
    *
    *  exports array to the byte buffer
    */
    """

    def export_array(self):
        # varying string: size = largest string
        if WsiBuffer.CLASS_VSA == self.d_class:
            self.__get_largest_string(self.m_value)
            self.size = self.largest

        # static array header
        self.msgb.put_array_header(self.d_type, self.d_class, self.size, self.scale, self.dim_ct, self.row_col)

        # dynamic array header
        self.__set_array_dimension(self.m_value)

        # dynamic array header
        self.__put_array_values(self.m_value)

    def export_array_by_wsi_buffer(self, new_buffer: 'WsiBuffer'):
        WsiUtils.check_type(new_buffer, WsiBuffer)
        self.msgb = new_buffer
        self.export_array()

    """
    /**
    * exportArrayValues
    *
    *  exports array values to the byte buffer (no Descriptor)
    */
    """

    def export_array_values(self, new_buffer: 'WsiBuffer'):
        WsiUtils.check_type(new_buffer, WsiBuffer)
        self.msgb = new_buffer
        self.__put_array_values(self.m_value)

    """
    /**
    *  importArray
    *
    *   reconstitutes array with updated values
    *
    */
    """

    def import_array(self):
        self.msgb.get_array_header()
        self.__get_array_values(self.m_value)

    def import_array_buffer(self, new_buffer: 'WsiBuffer'):
        self.msgb = new_buffer
        self.import_array()

    """
    /**
    * importArrayValues
    *
    *  exports array values to the byte buffer (no Descriptor)
    */
    """

    def import_array_values(self, new_buffer: 'WsiBuffer'):
        WsiUtils.check_type(new_buffer, WsiBuffer)
        self.msgb = new_buffer
        self.__get_array_values(self.m_value)

    def import_new_byte_array(self, new_buffer: 'WsiBuffer', array_size: int):
        WsiUtils.check_type(new_buffer, WsiBuffer)
        WsiUtils.check_type(array_size, int)
        self.m_value = [0] * array_size
        self.msgb = new_buffer
        self.import_array()

    """
    /**
    * Returns an element string
    */
    """

    def get_element_string(self):
        return ','.join(str(e) for e in self.dimensions)

    """
    /**
    * Throws exception if the text dimensions are not equal to the reflected
    * dimensions
    */
    """

    def __check_dimensions(self):
        str_ref_dim = self.get_element_string()
        if str_ref_dim.__eq__(self.str_dims) is False:
            raise Exception(
                "%WSI-E-INCBNDS - Bounds of passed in array (" + str_ref_dim + ") are inconsistent with those specified in IDL (" + self.str_dims + ").")

    """
    /**
    * Throws exception if the dimension count is not equal to the reflected
    * dimension count
    */
    """

    def __check_dim_count(self):
        if int(self.str_dims) != self.dim_ct:
            raise Exception(
                "%WSI-E-INCDIMCT - Dimension count specified in IDL is inconsistent with actual dimension count of the array.")

    """
    /**
    * Determines the number of elements per array dimension.
    *
    """

    def __set_dim_elements(self, s: object):
        for i in range(self.dim_ct):
            self.dimensions[i] = len(s)
            s = s[0]

    """
    /**
    * Determines number of dimensions of the array object.
    */
    """

    def __set_dimensions(self, s: object):
        if s is None:
            raise Exception("%WSI-E-INVAROBJ - Invalid array object type.")
        else:
            try:
                self.dim_ct = WsiUtils.array_deep(self.m_value)
            except IndexError:
                self.dim_ct = 1
            if self.dim_ct == 0:
                raise Exception("%WSI-E-INVARDIM - Invalid array dimension.")
    """
    /**
     *  Wrapper for bounds checking logic.
     */
    """
    def bounds_check_array(self):
        self.__set_dimensions(self.m_value)
        self.dimensions = [0]*self.dim_ct
        self.__set_dim_elements(self.m_value)
        if self.by_ref is True:
            self.__check_dimensions()
        else:
            self.__check_dim_count()
