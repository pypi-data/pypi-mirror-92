import pytest

from wsit.main.com.vsi.wsi.invalid_state_exception import InvalidStateException
from wsit.main.com.vsi.wsi.wsi_exception import WsiException
from wsit.test.com.vsi.wsi.wsi_exception_test import TestWsiException


class TestInvalidStateException:
    def test_init(self):
        invalid_state_exception = InvalidStateException()
        assert invalid_state_exception.get_status() == 0
        assert invalid_state_exception.get_facility() == 0
        assert invalid_state_exception.get_vms_status() == 0
        assert invalid_state_exception.get_severity() == 0

        assert invalid_state_exception.WSIsK_WARNING == 0
        assert invalid_state_exception.WSIsK_SUCCESS == 1
        assert invalid_state_exception.WSIsK_ERROR == 2
        assert invalid_state_exception.WSIsK_INFO == 3
        assert invalid_state_exception.WSIsK_SEVERE == 4
        assert invalid_state_exception.WSIsK_FAC_IPC == 1
        assert invalid_state_exception.WSIsK_FAC_RTL == 2
        assert invalid_state_exception.WSIsK_FAC_MGR == 3
        assert invalid_state_exception.WSIsK_FAC_SVR == 4

    def test_init_from_er_msg(self):
        for str_value in TestWsiException.str_valid_values:
            invalid_state_exception = InvalidStateException.init_from_er_msg(str_value)
            assert invalid_state_exception.get_message().__eq__(str_value)
            assert invalid_state_exception.get_status() == 0
            assert invalid_state_exception.get_facility() == 0
            assert invalid_state_exception.get_vms_status() == 0
            assert invalid_state_exception.get_severity() == 0
            assert isinstance(invalid_state_exception, WsiException) is True

    def test_private_field(self):
        invalid_state_exception = InvalidStateException()
        with pytest.raises(AttributeError):
            invalid_state_exception.value = 123
