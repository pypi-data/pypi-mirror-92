import pytest

from wsit.main.com.vsi.wsi.wsi_exception import WsiException
from wsit.main.com.vsi.wsi.wsi_server_exception import WsiServerException
from wsit.test.com.vsi.wsi.wsi_exception_test import TestWsiException


class TestWsiServerException:
    def test_init(self):
        wsi_server_exception = WsiServerException()
        assert wsi_server_exception.get_status() == 0
        assert wsi_server_exception.get_facility() == 0
        assert wsi_server_exception.get_vms_status() == 0
        assert wsi_server_exception.get_severity() == 0

        assert wsi_server_exception.WSIsK_WARNING == 0
        assert wsi_server_exception.WSIsK_SUCCESS == 1
        assert wsi_server_exception.WSIsK_ERROR == 2
        assert wsi_server_exception.WSIsK_INFO == 3
        assert wsi_server_exception.WSIsK_SEVERE == 4
        assert wsi_server_exception.WSIsK_FAC_IPC == 1
        assert wsi_server_exception.WSIsK_FAC_RTL == 2
        assert wsi_server_exception.WSIsK_FAC_MGR == 3
        assert wsi_server_exception.WSIsK_FAC_SVR == 4

        assert isinstance(wsi_server_exception, WsiException) is True

    def test_init_from_er_msg(self):
        for str_value in TestWsiException.str_valid_values:
            wsi_server_exception = WsiServerException.init_from_er_msg(str_value)
            assert wsi_server_exception.get_message().__eq__(str_value)
            assert wsi_server_exception.get_status() == 0
            assert wsi_server_exception.get_facility() == 0
            assert wsi_server_exception.get_vms_status() == 0
            assert wsi_server_exception.get_severity() == 0

    def test_init_from_er_msg_ex_code_vms_code(self):
        for str_value in TestWsiException.str_valid_values:
            for int_value in TestWsiException.int_valid_values:
                wsi_server_exception = WsiServerException.init_from_er_msg_ex_code_vms_code(str_value, int_value,
                                                                                            int_value)
                assert str_value.__eq__(wsi_server_exception.get_message())
                assert int_value == wsi_server_exception.get_status()
                assert int_value == wsi_server_exception.get_vms_status()

    def test_init_from_er_msg_ex_code_vms_code_severity_facility(self):
        for str_value in TestWsiException.str_valid_values:
            for int_value in TestWsiException.int_valid_values:
                for facility_value in TestWsiException.facility_values:
                    for severity_value in TestWsiException.severity_values:
                        wsi_server_exception = WsiServerException.init_from_er_msg_ex_code_vms_code_severity_facility(
                            str_value,
                            int_value, int_value,
                            severity_value,
                            facility_value)
                        assert str_value.__eq__(wsi_server_exception.get_message())
                        assert int_value == wsi_server_exception.get_status()
                        assert int_value == wsi_server_exception.get_vms_status()
                        assert severity_value == wsi_server_exception.get_severity()
                        assert facility_value == wsi_server_exception.get_facility()

    def test_private_field(self):
        wsi_server_exception = WsiServerException()
        with pytest.raises(AttributeError):
            wsi_server_exception.value = 123
