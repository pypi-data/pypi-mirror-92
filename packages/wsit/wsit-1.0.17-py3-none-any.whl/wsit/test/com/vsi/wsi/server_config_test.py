import pytest

from wsit.main.com.vsi.wsi.server_config import ServerConfig
from wsit.main.pyx.xml.rpc.holders.int_holder import IntHolder


class TestServerConfig:
    bind_valid_values = ["value", 'string', 'a', "b", "True", "False", "0", "1", '0', '1', '124.9090798',
                         '-0.126155', "-803485.9457897", "4564690846908.4059680458960", "485739857", "-4573875937"]
    bind_none_valid_values = ['', "", "None", 'None']
    str_exception_values = [True, False, 234.890, -7389457908.39485797, 23784629846, -98753948, 0, 1]
    int_valid_values = [IntHolder.MIN_VALUE, IntHolder.MAX_VALUE, 1234567890, IntHolder.MIN_VALUE + 1,
                        IntHolder.MAX_VALUE - 1]
    int_exception_values = ["value", 'string', 'a', "b", '', "", True, False, "True", "False", "0", "1", '0', '1',
                            928374.09748724, -0.000046537658736, '124.9090798', -45350.74658376578, '-0.126155',
                            "-803485.9457897", "4564690846908.4059680458960", "485739857", "-4573875937", None, "None", 'None']

    def test_init(self):
        server_config = ServerConfig()
        local = "Local"
        empty = ""
        assert empty.__eq__(server_config.get_app_name())
        assert empty.__eq__(server_config.get_app_uuid())
        assert empty.__eq__(server_config.get_tcp_ip_name())
        assert local.__eq__(server_config.get_scs_node_name())
        assert empty.__eq__(server_config.get_tx_tcp_ip_name())
        assert local.__eq__(server_config.get_tx_scs_node_name())
        assert empty.__eq__(server_config.get_binding())
        assert empty.__eq__(server_config.get_tx_binding())
        assert empty.__eq__(server_config.get_domain())
        assert server_config.is_app_multithreaded() is False
        assert server_config.is_transport() is True
        assert server_config.get_lease_timeout() == 60
        assert server_config.get_session_type() == ServerConfig.LIFETIME_SESSION
        assert server_config.get_major_version() == 1
        assert server_config.get_minor_version() == 0

    def test_set_binding_by_value(self):
        empty = ""
        for tested_value in TestServerConfig.bind_valid_values:
            server_config = ServerConfig()
            server_config.set_binding_by_value(tested_value)
            assert tested_value.__eq__(server_config.get_binding())
            assert tested_value.__eq__(server_config.get_tcp_ip_name())
            assert empty.__eq__(server_config.get_scs_node_name())
            assert server_config.is_transport() is True

    def test_set_binding_by_value_none(self):
        empty = ""
        for tested_value in TestServerConfig.bind_none_valid_values:
            server_config = ServerConfig()
            server_config.set_binding_by_value(tested_value)
            assert empty.__eq__(server_config.get_binding())
            assert tested_value.__eq__(server_config.get_tcp_ip_name())
            assert empty.__eq__(server_config.get_scs_node_name())
            assert server_config.is_transport() is False

    def test_set_binding_by_value_exception(self):
        server_config = ServerConfig()
        for tested_value in TestServerConfig.str_exception_values:
            with pytest.raises(TypeError):
                server_config.set_binding_by_value(tested_value)

    def test_set_binding_by_hosts(self):
        server_config = ServerConfig()
        local_ip_host = "127.0.0.1"
        tested_ip_host = "Local"
        tested_icc_host = "NotLocal"
        m_binding_string = "|wsi_icc:" + tested_icc_host
        m_binding_string = m_binding_string + "|" + "wsi_tcp:" + local_ip_host
        m_binding_string = m_binding_string + "|" + "ncadg_ip_udp:" + local_ip_host
        m_binding_string = m_binding_string + "|" + "ncacn_ip_tcp:" + local_ip_host + "|"
        server_config.set_binding_by_hosts(tested_ip_host, tested_icc_host)

        assert tested_ip_host.__eq__(server_config.get_tcp_ip_name())
        assert tested_icc_host.__eq__(server_config.get_scs_node_name())
        assert server_config.is_transport() is True
        assert m_binding_string.__eq__(server_config.get_binding())

    def test_set_binding_by_hosts_1(self):
        server_config = ServerConfig()
        tested_ip_host = "NotLocal"
        tested_icc_host = ""
        m_binding_string = "|" + "wsi_tcp:" + tested_ip_host
        m_binding_string = m_binding_string + "|" + "ncadg_ip_udp:" + tested_ip_host
        m_binding_string = m_binding_string + "|" + "ncacn_ip_tcp:" + tested_ip_host + "|"
        server_config.set_binding_by_hosts(tested_ip_host, tested_icc_host)
        assert tested_ip_host.__eq__(server_config.get_tcp_ip_name())
        assert tested_icc_host.__eq__(server_config.get_scs_node_name())
        assert server_config.is_transport() is True
        assert m_binding_string.__eq__(server_config.get_binding())

    def test_set_binding_by_hosts_2(self):
        server_config = ServerConfig()
        tested_ip_host = "None"
        tested_icc_host = "NotLocal"
        m_binding_string = "|" + "wsi_icc:" + tested_icc_host + "|"
        server_config.set_binding_by_hosts(tested_ip_host, tested_icc_host)
        assert tested_ip_host.__eq__(server_config.get_tcp_ip_name())
        assert tested_icc_host.__eq__(server_config.get_scs_node_name())
        assert server_config.is_transport() is True
        assert m_binding_string.__eq__(server_config.get_binding())

    def test_set_binding_by_hosts_3(self):
        server_config = ServerConfig()
        m_binding_string = ""
        for tested_ip_host in TestServerConfig.bind_none_valid_values:
            for tested_icc_host in TestServerConfig.bind_none_valid_values:
                server_config.set_binding_by_hosts(tested_ip_host, tested_icc_host)
                assert tested_ip_host.__eq__(server_config.get_tcp_ip_name())
                assert tested_icc_host.__eq__(server_config.get_scs_node_name())
                assert server_config.is_transport() is False
                assert m_binding_string.__eq__(server_config.get_binding())

    def test_set_binding_by_hosts_exception(self):
        server_config = ServerConfig()
        for tested_value in TestServerConfig.str_exception_values:
            with pytest.raises(TypeError):
                server_config.set_binding_by_hosts(tested_value, tested_value)

    def test_tx_binding_by_value(self):
        server_config = ServerConfig()
        server_config.set_binding_by_value("binding_string")
        for m_tx_binding_string in TestServerConfig.bind_valid_values:
            server_config.set_tx_binding_by_value(m_tx_binding_string)
            assert m_tx_binding_string.__eq__(server_config.get_tx_binding())
            assert not server_config.get_binding().__eq__(server_config.get_tx_binding())
            assert server_config.is_transport() is True

    def test_set_tx_binding_by_value_none(self):
        server_config = ServerConfig()
        server_config.set_binding_by_value("binding_string")
        for m_tx_binding_string in TestServerConfig.bind_none_valid_values:
            server_config.set_tx_binding_by_value(m_tx_binding_string)
            assert server_config.get_tx_binding().__eq__(server_config.get_binding())
            assert server_config.is_transport() is True

    def test_set_tx_binding_by_value_exception(self):
        server_config = ServerConfig()
        for tested_value in TestServerConfig.str_exception_values:
            with pytest.raises(TypeError):
                server_config.set_tx_binding_by_value(tested_value)

    def test_set_tx_binding_by_hosts(self):
        server_config = ServerConfig()
        for tested_value in TestServerConfig.bind_valid_values:
            ip_host_string = icc_host_string = tested_value
            m_tx_binding = "|" + "wsi_icc:" + icc_host_string
            m_tx_binding = m_tx_binding + "|" + "wsi_tcp:" + ip_host_string
            m_tx_binding = m_tx_binding + "|" + "ncadg_ip_udp:" + ip_host_string
            m_tx_binding = m_tx_binding + "|" + "ncacn_ip_tcp:" + ip_host_string + "|"
            server_config.set_tx_binding_by_hosts(ip_host_string, icc_host_string)
            assert m_tx_binding.__eq__(server_config.get_tx_binding())

    def test_set_tx_binding_by_hosts_1(self):
        for ip_host_string in TestServerConfig.bind_valid_values:
            for icc_host_string in TestServerConfig.bind_none_valid_values:
                server_config = ServerConfig()
                m_tx_binding = "|" + "wsi_tcp:" + ip_host_string
                m_tx_binding = m_tx_binding + "|" + "ncadg_ip_udp:" + ip_host_string
                m_tx_binding = m_tx_binding + "|" + "ncacn_ip_tcp:" + ip_host_string + "|"
                server_config.set_tx_binding_by_hosts(ip_host_string, icc_host_string)
                assert m_tx_binding.__eq__(server_config.get_tx_binding())

    def test_set_tx_binding_by_hosts_2(self):
        for none_value in TestServerConfig.bind_none_valid_values:
            server_config = ServerConfig()
            ip_host_string = icc_host_string = none_value
            m_tx_binding = ""
            server_config.set_tx_binding_by_hosts(ip_host_string, icc_host_string)
            assert m_tx_binding.__eq__(server_config.get_tx_binding())

    def test_set_tx_binding_by_hosts_exception(self):
        server_config = ServerConfig()
        for tested_value in TestServerConfig.str_exception_values:
            with pytest.raises(TypeError):
                server_config.set_tx_binding_by_hosts(tested_value, tested_value)

    def test_set_major_version(self):
        server_config = ServerConfig()
        for tested_value in TestServerConfig.int_valid_values:
            server_config.set_major_version(tested_value)
            assert tested_value.__eq__(server_config.get_major_version())

    def test_set_major_version_exception(self):
        server_config = ServerConfig()
        for tested_value in TestServerConfig.int_exception_values:
            with pytest.raises(TypeError):
                server_config.set_major_version(tested_value)

    def test_set_minor_version(self):
        server_config = ServerConfig()
        for tested_value in TestServerConfig.int_valid_values:
            server_config.set_minor_version(tested_value)
            assert tested_value == server_config.get_minor_version()

    def test_set_minor_version_exception(self):
        server_config = ServerConfig()
        for tested_value in TestServerConfig.int_exception_values:
            with pytest.raises(TypeError):
                server_config.set_minor_version(tested_value)

    def test_set_lease_timeout(self):
        server_config = ServerConfig()
        for tested_value in TestServerConfig.int_valid_values:
            server_config.set_lease_timeout(tested_value)
            assert tested_value == server_config.get_lease_timeout()

    def test_set_lease_timeout_exception(self):
        server_config = ServerConfig()
        for tested_value in TestServerConfig.int_exception_values:
            with pytest.raises(TypeError):
                server_config.set_lease_timeout(tested_value)

    def test_is_local(self):
        server_config = ServerConfig()
        assert server_config.is_local() is True  # with __m_ip_host_name eq None
        for m_ip_host_name in ["", "LOCALhost", "localHost", "LoCalHosT"]:
            server_config.set_tcp_ip_name(m_ip_host_name)
            assert server_config.is_local() is True

        for m_ip_host_name in TestServerConfig.bind_valid_values:
            server_config.set_tcp_ip_name(m_ip_host_name)
            assert server_config.is_local() is False

    def test_set_app_name(self):
        server_config = ServerConfig()
        for tested_value in TestServerConfig.bind_valid_values:
            server_config.set_app_name(tested_value)
            assert tested_value.__eq__(server_config.get_app_name())

    def test_set_app_name_exception(self):
        server_config = ServerConfig()
        for tested_value in TestServerConfig.str_exception_values:
            with pytest.raises(TypeError):
                server_config.set_app_name(tested_value)

    def test_set_app_uuid(self):
        server_config = ServerConfig()
        for tested_value in TestServerConfig.bind_valid_values:
            server_config.set_app_uuid(tested_value)
            assert tested_value.__eq__(server_config.get_app_uuid())

    def test_set_app_uuid_exception(self):
        server_config = ServerConfig()
        for tested_value in TestServerConfig.str_exception_values:
            with pytest.raises(TypeError):
                server_config.set_app_uuid(tested_value)

    def test_set_domain(self):
        server_config = ServerConfig()
        for tested_value in TestServerConfig.bind_valid_values:
            server_config.set_domain(tested_value)
            assert tested_value.__eq__(server_config.get_domain())

    def test_set_domain_exception(self):
        server_config = ServerConfig()
        for tested_value in TestServerConfig.str_exception_values:
            with pytest.raises(TypeError):
                server_config.set_domain(tested_value)

    def test_set_session_type_value_int(self):
        server_config = ServerConfig()
        for tested_value in [ServerConfig.NO_SESSION, ServerConfig.TX_SESSION, ServerConfig.LIFETIME_SESSION, ServerConfig.TX_LIFETIME]:
            server_config.set_session_type_int(tested_value)
            assert tested_value == server_config.get_session_type()

    def test_set_session_type_value_int_exception(self):
        server_config = ServerConfig()
        for tested_value in TestServerConfig.int_valid_values:
            with pytest.raises(AttributeError):
                server_config.set_session_type_int(tested_value)

    def test_set_session_type_value_int_exception_1(self):
        server_config = ServerConfig()
        for tested_value in TestServerConfig.bind_valid_values:
            with pytest.raises(TypeError):
                server_config.set_session_type_int(tested_value)

    def test_set_session_type_value_str(self):
        server_config = ServerConfig()
        session_types = [ServerConfig.NO_SESSION, ServerConfig.TX_SESSION, ServerConfig.LIFETIME_SESSION, ServerConfig.TX_LIFETIME]
        session_values = ["no_session", "tx_session", "lifetime_session", "tx_lifetime"]
        for i in range(len(session_types)):
            server_config.set_session_type_str(session_values[i])
            assert session_types[i] == server_config.get_session_type()

    def test_set_session_type_value_exception(self):
        server_config = ServerConfig()
        for tested_value in TestServerConfig.bind_valid_values:
            with pytest.raises(AttributeError):
                server_config.set_session_type_str(tested_value)

    def test_set_session_type_value_exception_1(self):
        server_config = ServerConfig()
        for tested_value in TestServerConfig.int_valid_values:
            with pytest.raises(TypeError):
                server_config.set_session_type_str(tested_value)

    def test_to_string(self):
        server_config = ServerConfig()
        for tested_value in TestServerConfig.bind_valid_values:
            server_config.set_binding_by_value(tested_value)
            server_config.set_app_name(tested_value)
            for session_value in ["no_session", "tx_session", "lifetime_session", "tx_lifetime"]:
                server_config.set_session_type_str(session_value)
                to_string = "ServerConfig: mBinding = " + str(server_config.get_binding())\
                            + ", appName = " + str(server_config.get_app_name()) +\
                            ", sessionType = " + str(server_config.get_session_type())
                assert to_string.__eq__(server_config.to_string())

    def test_set_tcp_ip_name(self):
        server_config = ServerConfig()
        for tested_value in TestServerConfig.bind_valid_values:
            server_config.set_tcp_ip_name(tested_value)
            assert tested_value.__eq__(server_config.get_tcp_ip_name())

    def test_set_tcp_ip_name_exception(self):
        server_config = ServerConfig()
        for tested_value in TestServerConfig.str_exception_values:
            with pytest.raises(TypeError):
                server_config.set_tcp_ip_name(tested_value)

    def test_set_scs_node_name(self):
        server_config = ServerConfig()
        for tested_value in TestServerConfig.bind_valid_values:
            server_config.set_scs_node_name(tested_value)
            assert tested_value.__eq__(server_config.get_scs_node_name())

    def test_set_scs_node_name_exception(self):
        server_config = ServerConfig()
        for tested_value in TestServerConfig.str_exception_values:
            with pytest.raises(TypeError):
                server_config.set_scs_node_name(tested_value)

    def test_set_tx_tcp_ip_name(self):
        server_config = ServerConfig()
        for tested_value in TestServerConfig.bind_valid_values:
            server_config.set_tx_tcp_ip_name(tested_value)
            assert tested_value.__eq__(server_config.get_tx_tcp_ip_name())

    def test_set_tx_tcp_ip_name_exception(self):
        server_config = ServerConfig()
        for tested_value in TestServerConfig.str_exception_values:
            with pytest.raises(TypeError):
                server_config.set_tx_tcp_ip_name(tested_value)

    def test_set_tx_scs_node_name(self):
        server_config = ServerConfig()
        for tested_value in TestServerConfig.bind_valid_values:
            server_config.set_tx_scs_node_name(tested_value)
            assert tested_value.__eq__(server_config.get_tx_scs_node_name())

    def test_set_tx_scs_node_name_exception(self):
        server_config = ServerConfig()
        for tested_value in TestServerConfig.str_exception_values:
            with pytest.raises(TypeError):
                server_config.set_tx_scs_node_name(tested_value)

    def test_private_field(self):
        server_config = ServerConfig()
        with pytest.raises(AttributeError):
            server_config.value = 123
