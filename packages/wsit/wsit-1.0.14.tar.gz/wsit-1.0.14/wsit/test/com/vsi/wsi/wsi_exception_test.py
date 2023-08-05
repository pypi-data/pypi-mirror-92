import pytest

from wsit.main.com.vsi.wsi.wsi_exception import WsiException
from wsit.main.pyx.xml.rpc.holders.int_holder import IntHolder


class TestWsiException:
    str_valid_values = ["selection string", 'selection string', "a", 'b', "", "True", "False", "0", '0', "1", '1',
                        '124.9090798', '-0.126155', "-803485.9457897", "4564690846908.4059680458960", "485739857",
                        "-4573875937", "None", 'None']
    exception_valid_values = [ArithmeticError(), TypeError(), ValueError()]

    int_valid_values = [1, 2, 3, 4, 5, 6, 0, -1, -2, -3, -4, -5, -6]

    exception_int_values = [IntHolder.MIN_VALUE - 1, IntHolder.MAX_VALUE + 1, "value", 'string', 'a', "b", '', "", True,
                            False, "True", "False", "0", "1", '0', '1', -84563865890, 928374.09748724,
                            -0.000046537658736,
                            '124.9090798', -45350.74658376578, '-0.126155', "-803485.9457897",
                            "4564690846908.4059680458960", "485739857", "-4573875937", None, "None", 'None']

    exception_text_values = [-97038573098, 8470750398475, True, False, 234.890, -7389457908.39485797, None]

    facility_values = [WsiException.WSIsK_FAC_IPC, WsiException.WSIsK_FAC_RTL, WsiException.WSIsK_FAC_MGR,
                       WsiException.WSIsK_FAC_SVR]

    severity_values = [WsiException.WSIsK_WARNING, WsiException.WSIsK_SUCCESS, WsiException.WSIsK_ERROR,
                       WsiException.WSIsK_INFO, WsiException.WSIsK_SEVERE]

    def test_init(self):
        wsi_exception = WsiException()
        assert wsi_exception.get_status() == 0
        assert wsi_exception.get_facility() == 0
        assert wsi_exception.get_vms_status() == 0
        assert wsi_exception.get_severity() == 0

        assert WsiException.WSIsK_WARNING == 0
        assert WsiException.WSIsK_SUCCESS == 1
        assert WsiException.WSIsK_ERROR == 2
        assert WsiException.WSIsK_INFO == 3
        assert WsiException.WSIsK_SEVERE == 4
        assert WsiException.WSIsK_FAC_IPC == 1
        assert WsiException.WSIsK_FAC_RTL == 2
        assert WsiException.WSIsK_FAC_MGR == 3
        assert WsiException.WSIsK_FAC_SVR == 4

    def test_init_from_er_msg(self):
        for tested_value in TestWsiException.str_valid_values:
            wsi_exception = WsiException.init_from_er_msg(tested_value)
            assert wsi_exception.get_message() == tested_value
            assert wsi_exception.get_status() == 0
            assert wsi_exception.get_facility() == 0
            assert wsi_exception.get_vms_status() == 0
            assert wsi_exception.get_severity() == 0

    def test_init_from_er_msg_exception(self):
        for tested_value in TestWsiException.exception_text_values:
            with pytest.raises(TypeError):
                wsi_exception = WsiException.init_from_er_msg(tested_value)

    def test_init_from_er_msg_except(self):
        for except_values in TestWsiException.exception_valid_values:
            for tested_value in TestWsiException.str_valid_values:
                wsi_exception = WsiException.init_from_er_msg_except(except_values, tested_value)
                assert except_values.__eq__(wsi_exception.get_detail())
                assert tested_value.__eq__(wsi_exception.get_message())

    def test_init_from_er_msg_except_exception(self):
        for tested_value in TestWsiException.exception_text_values:
            for int_value in TestWsiException.exception_int_values:
                with pytest.raises(TypeError):
                    wsi_exception = WsiException.init_from_er_msg_except(tested_value, int_value)

    def test_init_from_except(self):
        for except_values in TestWsiException.exception_valid_values:
            wsi_exception = WsiException.init_from_except(except_values)
            assert except_values.__eq__(wsi_exception.get_detail())

    # only Exception type
    def test_init_from_except_exception(self):
        for tested_value in TestWsiException.str_valid_values + TestWsiException.int_valid_values + TestWsiException.exception_int_values + TestWsiException.exception_text_values:
            with pytest.raises(TypeError):
                wsi_exception = WsiException.init_from_except(tested_value)

    def test_init_from_er_msg_ex_code_vms_code(self):
        for tested_value in TestWsiException.str_valid_values:
            for int_value in TestWsiException.int_valid_values:
                wsi_exception = WsiException.init_from_er_msg_ex_code_vms_code(tested_value, int_value, int_value)
                assert tested_value.__eq__(wsi_exception.get_message())
                assert int_value == wsi_exception.get_status()
                assert int_value == wsi_exception.get_vms_status()

    def test_init_from_er_msg_ex_code_vms_code_exception(self):
        for int_value in TestWsiException.exception_int_values:
            for text_value in TestWsiException.exception_text_values:
                with pytest.raises(TypeError):
                    wsi_exception = WsiException.init_from_er_msg_ex_code_vms_code(text_value, int_value, int_value)

    def test_init_from_er_msg_ex_code_vms_code_severity_facility(self):
        for str_value in TestWsiException.str_valid_values:
            for int_value in TestWsiException.int_valid_values:
                for facility_value in TestWsiException.facility_values:
                    for severity_value in TestWsiException.severity_values:
                        wsi_exception = WsiException.init_from_er_msg_ex_code_vms_code_severity_facility(str_value,
                                                                                                         int_value,
                                                                                                         int_value,
                                                                                                         severity_value,
                                                                                                         facility_value)
                        assert str_value.__eq__(wsi_exception.get_message())
                        assert int_value == wsi_exception.get_status()
                        assert int_value == wsi_exception.get_vms_status()
                        assert severity_value == wsi_exception.get_severity()
                        assert facility_value == wsi_exception.get_facility()

    def test_init_from_er_msg_ex_code_vms_code_severity_facility_exception(self):
        for int_value in TestWsiException.exception_int_values:
            for text_value in TestWsiException.exception_text_values:
                with pytest.raises(TypeError):
                    wsi_exception = WsiException.init_from_er_msg_ex_code_vms_code_severity_facility(text_value,
                                                                                                     int_value,
                                                                                                     int_value,
                                                                                                     int_value,
                                                                                                     int_value)

    def test_init_from_wsi_ex(self):
        for str_value in TestWsiException.str_valid_values:
            for int_value in TestWsiException.int_valid_values:
                wsi_exception = WsiException.init_from_er_msg_ex_code_vms_code_severity_facility(str_value, int_value,
                                                                                                 int_value,
                                                                                                 int_value,
                                                                                                 int_value)
                wsi_exception_other = WsiException.init_from_wsi_exception(wsi_exception)
                assert str_value.__eq__(wsi_exception_other.get_message())
                assert int_value == wsi_exception_other.get_status()
                assert int_value == wsi_exception_other.get_vms_status()
                assert int_value == wsi_exception_other.get_severity()
                assert int_value == wsi_exception_other.get_facility()

    # only Wsi Exception type
    def test_init_from_wsi_ex_exception(self):
        for tested_value in TestWsiException.str_valid_values + TestWsiException.int_valid_values + TestWsiException.exception_int_values + TestWsiException.exception_text_values:
            with pytest.raises(TypeError):
                wsi_exception = WsiException.init_from_wsi_exception(tested_value)

    def test_is_connection_valid(self):
        in_exc_code_test = 1
        in_vms_code_test = 1
        in_severity_test = WsiException.WSIsK_INFO
        in_facility_test = WsiException.WSIsK_FAC_MGR
        er_message = "Error message"

        wsi_exception = WsiException.init_from_er_msg_ex_code_vms_code_severity_facility(er_message, in_exc_code_test,
                                                                                         in_vms_code_test,
                                                                                         in_severity_test,
                                                                                         in_facility_test)
        assert wsi_exception.is_connection_valid() is False

        in_facility_test = WsiException.WSIsK_FAC_IPC
        in_severity_test = WsiException.WSIsK_SEVERE
        wsi_exception = WsiException.init_from_er_msg_ex_code_vms_code_severity_facility(er_message,
                                                                                         in_exc_code_test,
                                                                                         in_vms_code_test,
                                                                                         in_severity_test,
                                                                                         in_facility_test)
        assert wsi_exception.is_connection_valid() is False

        in_facility_test = WsiException.WSIsK_FAC_RTL
        in_severity_test = WsiException.WSIsK_SEVERE
        wsi_exception = WsiException.init_from_er_msg_ex_code_vms_code_severity_facility(er_message,
                                                                                         in_exc_code_test,
                                                                                         in_vms_code_test,
                                                                                         in_severity_test,
                                                                                         in_facility_test)
        assert wsi_exception.is_connection_valid() is True

        in_facility_test = WsiException.WSIsK_FAC_IPC
        in_severity_test = WsiException.WSIsK_INFO
        wsi_exception = WsiException.init_from_er_msg_ex_code_vms_code_severity_facility(er_message,
                                                                                         in_exc_code_test,
                                                                                         in_vms_code_test,
                                                                                         in_severity_test,
                                                                                         in_facility_test)
        assert wsi_exception.is_connection_valid() is True

        in_facility_test = WsiException.WSIsK_FAC_RTL
        wsi_exception = WsiException.init_from_er_msg_ex_code_vms_code_severity_facility(er_message,
                                                                                         in_exc_code_test,
                                                                                         in_vms_code_test,
                                                                                         in_severity_test,
                                                                                         in_facility_test)
        assert wsi_exception.is_connection_valid() is True

    def test_private_field(self):
        wsi_exception = WsiException()
        with pytest.raises(AttributeError):
            wsi_exception.value = 123
