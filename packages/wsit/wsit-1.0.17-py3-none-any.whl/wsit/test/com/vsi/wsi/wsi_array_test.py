import pytest

from wsit.main.com.vsi.wsi.wsi_array import WsiArray


class TestWsiArray:
    def test_init(self):
        wsi_array = WsiArray()
        assert wsi_array.get_value() is None

    def test_init_by_m_value(self):
        tested_value = "test"
        wsi_array = WsiArray.init_by_m_value(tested_value)
        assert wsi_array.get_value() == tested_value

    def test_init_by_all_vars(self):
        m_value = [["test1", "test2", "test3"], ["test4", "test5", "test6"]]
        from wsit.main.com.vsi.wsi.wsi_buffer import WsiBuffer
        msgb = WsiBuffer()
        d_type = 0
        d_class = 12
        size = 0
        scale = 0
        row_col = False
        null_term = 0
        str_dims = "2"
        by_ref = False
        dimensions = [2, 3]
        dim_ct = 2
        wsi_array = WsiArray.init_by_all_vars(m_value, msgb, d_type, d_class, size, scale, row_col, null_term, str_dims, by_ref)
        assert wsi_array.get_value() == m_value
        assert wsi_array.dim_ct == dim_ct
        assert wsi_array.dimensions == dimensions

    def test_init_by_all_vrs_is_wsi_array(self):
        m_value = [["test1", "test2", "test3"], ["test4", "test5", "test6"]]
        from wsit.main.com.vsi.wsi.wsi_buffer import WsiBuffer
        msgb = WsiBuffer()
        d_type = 0
        d_class = 12
        size = 0
        scale = 0
        row_col = False
        null_term = 0
        str_dims = "2"
        by_ref = False
        is_wsi_array = True
        dimensions = [2, 3]
        dim_ct = 2
        wsi_array = WsiArray.init_by_all_vars_is_wsi_array(m_value, msgb, d_type, d_class, size, scale, row_col, null_term, str_dims,
                                              by_ref, is_wsi_array)
        assert wsi_array.get_value() == m_value
        assert wsi_array.dim_ct == dim_ct
        assert wsi_array.dimensions == dimensions

    def test_set_value(self):
        m_value = [["test1", "test2", "test3"], ["test4", "test5", "test6"]]
        wsi_array = WsiArray()
        wsi_array.set_value(m_value)
        assert wsi_array.get_value() == m_value

    def test_bounds_check_array_exception(self):
        wsi_array = WsiArray()
        with pytest.raises(Exception):
            wsi_array.bounds_check_array()

    def test_bounds_check_array_exception_2(self):
        m_value = "test1"
        wsi_array = WsiArray.init_by_m_value(m_value)
        with pytest.raises(Exception):
            wsi_array.bounds_check_array()

    def test_bounds_check_array_exception_3(self):
        m_value = [["test1", "test2", "test3"], ["test4", "test5", "test6"]]
        from wsit.main.com.vsi.wsi.wsi_buffer import WsiBuffer
        msgb = WsiBuffer()
        d_type = 0
        d_class = 12
        size = 0
        scale = 0
        row_col = False
        null_term = 0
        str_dims = "3"
        by_ref = False
        is_wsi_array = True
        with pytest.raises(Exception):
            wsi_array = WsiArray.init_by_all_vars_is_wsi_array(m_value, msgb, d_type, d_class, size, scale, row_col, null_term, str_dims,
                                              by_ref, is_wsi_array)

    def test_bounds_check_array_exception_4(self):
        m_value = [["test1", "test2", "test3"], ["test4", "test5", "test6"]]
        from wsit.main.com.vsi.wsi.wsi_buffer import WsiBuffer
        msgb = WsiBuffer()
        d_type = 0
        d_class = 12
        size = 0
        scale = 0
        row_col = False
        null_term = 0
        str_dims = "3"
        by_ref = True
        is_wsi_array = True
        with pytest.raises(Exception):
            wsi_array = WsiArray.init_by_all_vars_is_wsi_array(m_value, msgb, d_type, d_class, size, scale, row_col, null_term, str_dims,
                                              by_ref, is_wsi_array)

    def test_export_array_by_wsi_buffer(self):
        strings = ["test1", "test2"]
        wsi_array = WsiArray.init_by_m_value(strings)
        from wsit.main.com.vsi.wsi.wsi_buffer import WsiBuffer
        wsi_buffer = WsiBuffer()
        wsi_buffer.put_str_ary_d_type_len_null_term(strings,WsiBuffer.DTYPE_T, len(strings), 0)
        wsi_array.d_type = WsiBuffer.DTYPE_T
        wsi_array.export_array_by_wsi_buffer(wsi_buffer)
        assert wsi_array.msgb.__eq__(wsi_buffer)

    def test_export_array_values(self):
        strings = ["test1", "test2"]
        wsi_array = WsiArray.init_by_m_value(strings)
        from wsit.main.com.vsi.wsi.wsi_buffer import WsiBuffer
        wsi_buffer = WsiBuffer()
        wsi_buffer.put_str_ary_d_type_len_null_term(strings,WsiBuffer.DTYPE_T, len(strings), 0)
        wsi_array.d_type = WsiBuffer.DTYPE_T
        wsi_array.export_array_values(wsi_buffer)
        assert wsi_array.msgb.__eq__(wsi_buffer)