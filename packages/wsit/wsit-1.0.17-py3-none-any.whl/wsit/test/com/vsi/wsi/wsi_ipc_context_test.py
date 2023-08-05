import pytest

from wsit.main.com.vsi.wsi.wsi_ipc_context import WsiIpcContext
from wsit.test.com.vsi.wsi.server_config_test import TestServerConfig


class TestWsiIpcContext(TestServerConfig):
    @staticmethod
    def param_check(wsi_object):
        local = "Local"
        empty = ""
        assert empty.__eq__(wsi_object.get_app_name())
        assert empty.__eq__(wsi_object.get_app_uuid())
        assert empty.__eq__(wsi_object.get_tcp_ip_name())
        assert local.__eq__(wsi_object.get_scs_node_name())
        assert empty.__eq__(wsi_object.get_tx_tcp_ip_name())
        assert local.__eq__(wsi_object.get_tx_scs_node_name())
        assert empty.__eq__(wsi_object.get_binding())
        assert empty.__eq__(wsi_object.get_tx_binding())
        assert empty.__eq__(wsi_object.get_domain())
        assert wsi_object.is_app_multithreaded() is False
        assert wsi_object.is_transport() is True
        assert wsi_object.get_major_version() == 1
        assert wsi_object.get_minor_version() == 0

    def test_init(self):
        wsi_ipc_context = WsiIpcContext()
        TestWsiIpcContext.param_check(wsi_ipc_context)
        assert wsi_ipc_context.get_lease_timeout() == 60
        assert wsi_ipc_context.get_session_type() == WsiIpcContext.LIFETIME_SESSION

    def test_init_by_stype_lease(self):
        for tested_value in [WsiIpcContext.NO_SESSION, WsiIpcContext.TX_SESSION, WsiIpcContext.LIFETIME_SESSION,
                             WsiIpcContext.TX_LIFETIME]:
            for i in TestServerConfig.int_valid_values:
                wsi_ipc_context = WsiIpcContext.init_by_stype_lease(tested_value, i)
                TestWsiIpcContext.param_check(wsi_ipc_context)
                assert tested_value.__eq__(wsi_ipc_context.get_session_type())
                assert i == wsi_ipc_context.get_lease_timeout()

    def test_init_by_sesstype_lease(self):
        for tested_value in ["LIFETIME_SESSION", "TX_LIFETIME"]:
            for i in TestServerConfig.int_valid_values:
                wsi_ipc_context = WsiIpcContext.init_by_sesstype_lease(tested_value, i)
                TestWsiIpcContext.param_check(wsi_ipc_context)
                assert WsiIpcContext.LIFETIME_SESSION.__eq__(wsi_ipc_context.get_session_type())
                assert i == wsi_ipc_context.get_lease_timeout()

    def test_init_by_sesstype_lease_1(self):
        for i in TestServerConfig.int_valid_values:
            wsi_ipc_context = WsiIpcContext.init_by_sesstype_lease("NO_SESSION", i)
            TestWsiIpcContext.param_check(wsi_ipc_context)
            assert WsiIpcContext.NO_SESSION.__eq__(wsi_ipc_context.get_session_type())
            assert i == wsi_ipc_context.get_lease_timeout()

    def test_init_by_sesstype_lease_2(self):
        for i in TestServerConfig.int_valid_values:
            wsi_ipc_context = WsiIpcContext.init_by_sesstype_lease("TX_SESSION", i)
            TestWsiIpcContext.param_check(wsi_ipc_context)
            assert WsiIpcContext.TX_SESSION.__eq__(wsi_ipc_context.get_session_type())
            assert i == wsi_ipc_context.get_lease_timeout()

    def test_init_by_sesstype_lease_exception(self):
        for i in TestServerConfig.int_valid_values:
            with pytest.raises(TypeError):
                wsi_ipc_context = WsiIpcContext.init_by_sesstype_lease(i, i)

    def test_set_session_type(self):
        wsi_ipc_context = WsiIpcContext()
        for tested_value in [WsiIpcContext.NO_SESSION, WsiIpcContext.TX_SESSION, WsiIpcContext.LIFETIME_SESSION,
                             WsiIpcContext.TX_LIFETIME]:
            wsi_ipc_context.set_session_type_int(tested_value)
            TestWsiIpcContext.param_check(wsi_ipc_context)
            assert tested_value.__eq__(wsi_ipc_context.get_session_type())

    def test_set_lease_timeout(self):
        wsi_ipc_context = WsiIpcContext()
        for i in TestServerConfig.int_valid_values:
            wsi_ipc_context.set_lease_timeout(i)
            TestWsiIpcContext.param_check(wsi_ipc_context)
            assert i == wsi_ipc_context.get_lease_timeout()

    def test_private_field(self):
        wsi_ipc_context = WsiIpcContext()
        with pytest.raises(AttributeError):
            wsi_ipc_context.value = 123