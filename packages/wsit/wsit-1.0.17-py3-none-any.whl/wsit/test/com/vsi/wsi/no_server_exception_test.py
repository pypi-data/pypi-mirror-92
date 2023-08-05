import pytest

from wsit.main.com.vsi.wsi.no_server_exception import NoServerException
from wsit.main.com.vsi.wsi.wsi_exception import WsiException
from wsit.test.com.vsi.wsi.wsi_exception_test import TestWsiException


class TestNoServerException:
    def test_init(self):
        no_server_exception = NoServerException()
        assert no_server_exception.get_status() == 0
        assert no_server_exception.get_facility() == 0
        assert no_server_exception.get_vms_status() == 0
        assert no_server_exception.get_severity() == 0

        assert no_server_exception.WSIsK_WARNING == 0
        assert no_server_exception.WSIsK_SUCCESS == 1
        assert no_server_exception.WSIsK_ERROR == 2
        assert no_server_exception.WSIsK_INFO == 3
        assert no_server_exception.WSIsK_SEVERE == 4
        assert no_server_exception.WSIsK_FAC_IPC == 1
        assert no_server_exception.WSIsK_FAC_RTL == 2
        assert no_server_exception.WSIsK_FAC_MGR == 3
        assert no_server_exception.WSIsK_FAC_SVR == 4

    def test_init_from_er_msg(self):
        for str_value in TestWsiException.str_valid_values:
            no_server_exception = NoServerException.init_from_er_msg(str_value)
            assert no_server_exception.get_message().__eq__(str_value)
            assert no_server_exception.get_status() == 0
            assert no_server_exception.get_facility() == 0
            assert no_server_exception.get_vms_status() == 0
            assert no_server_exception.get_severity() == 0
            assert isinstance(no_server_exception, WsiException) is True

    def test_private_field(self):
        no_server_exception = NoServerException()
        with pytest.raises(AttributeError):
            no_server_exception.value = 123
