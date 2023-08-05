"""An instance of this class contains all the configuration information needed
   to start up and initialize the native server(s) for an EIS.  All of these
   attributes are settable by the application deployer, and not hardwired into
   any code module.
"""
from wsit.main.com.vsi.wsi.wsi_utils import WsiUtils


class ServerConfig:
    # Names for the properties used by the property change listeners
    __PROP_HOSTNAME = "HostName"
    __PROP_BINDING = "Binding"
    __PROP_TXBINDING = "TxBinding"
    __PROP_APPNAME = "AppName"
    __PROP_APPUUID = "AppUuid"
    __PROP_DOMAIN = "Domain"
    __PROP_MAJOR_VERSION = "MajorVersion"
    __PROP_MINOR_VERSION = "MinorVersion"
    __PROP_SESSION_TYPE = "SessionType"
    __PROP_LEASETIMEOUT = "LeaseTimeout"

    NO_SESSION = 0
    TX_SESSION = 1
    LIFETIME_SESSION = 2
    TX_LIFETIME = 3

    __m_app_name = ""
    __m_app_uuid = ""
    __m_ip_host_name = ""
    __m_icc_host_name = "Local"
    __m_tx_ip_host_name = ""
    __m_tx_icc_host_name = "Local"
    __m_binding = ""
    __m_tx_binding = ""
    __m_domain = ""
    __m_is_app_multithreaded = False
    __m_is_transport = True
    __m_max_app_threads = 1
    __m_lease_timeout = 60
    __m_session_type = LIFETIME_SESSION
    __m_major_version = 1
    __m_minor_version = 0

    """ Retrieve the Binding property.  The Binding property indicates the
        connection binding being used to connect to the server.
            |ncacn_ip_tcp:16.32.0.1|wsicn_icc:GALAXY|
        <p>
        Note that value of "" is considered special, and indicate
        that the user's sharable will be loaded into the current process.
        @return Name of the binding to locate the server.
        @see #setBinding(String)
        @see #isLocal()
    """

    def get_binding(self) -> str:
        return self.__m_binding

    """ Update the Binding property
        @param value     New value for the Binding property
        @see #getBinding()
        @see #isNonTransport()
    """

    def set_binding_by_value(self, value: str):
        WsiUtils.check_type(value, str)
        # old = self.__m_binding
        self.__m_binding = ""
        self.__m_ip_host_name = value
        self.__m_icc_host_name = ""
        # Special case None as meaning that no transport will be used.
        if not value.__eq__("None"):
            self.__m_binding = value

        if self.__m_binding.__eq__(""):
            self.__m_is_transport = False
        else:
            self.__m_is_transport = True

    def set_binding_by_hosts(self, ip_host: str, icc_host: str):
        WsiUtils.check_type(ip_host, str)
        WsiUtils.check_type(icc_host, str)
        self.__m_binding = ""

        self.__m_ip_host_name = ip_host
        self.__m_icc_host_name = icc_host

        if ip_host.__eq__("Local"):
            ip_host = "127.0.0.1"

        # if icc_host.__eq__("Local"):
        #     icc_host = WsiJNIShell.getNodeName();

        if not icc_host.__eq__("None") and not icc_host.__eq__(""):
            self.__m_binding = "|" + "wsi_icc:" + icc_host

        if not ip_host.__eq__("None") and not ip_host.__eq__(""):
            self.__m_binding = self.__m_binding + "|" + "wsi_tcp:" + ip_host
            self.__m_binding = self.__m_binding + "|" + "ncadg_ip_udp:" + ip_host
            self.__m_binding = self.__m_binding + "|" + "ncacn_ip_tcp:" + ip_host

        if self.__m_binding.__eq__(""):
            self.__m_is_transport = False
        else:
            self.__m_binding = self.__m_binding + "|"  # terminating bar
            self.__m_is_transport = True

    def set_binding(self):
        self.set_binding_by_hosts(self.__m_ip_host_name, self.__m_icc_host_name)

    """ Retrieve the TX Binding property.  The Binding property indicates the
        connection binding being used to connect to the commitment server.
             |ncacn_ip_tcp:16.32.0.1|wsicn_icc:GALAXY|
        
          @return Name of the binding to locate the server.
          @see #setTxBinding(String)
          @see #isLocal()
    """

    def get_tx_binding(self) -> str:
        if self.__m_tx_binding.__eq__(""):
            return self.__m_binding
        return self.__m_tx_binding

    """ Update the Binding property
        
          @param value     New value for the Binding property

          @see #getBinding()
          @see #isNonTransport()
    """

    def set_tx_binding_by_value(self, value: str):
        WsiUtils.check_type(value, str)
        self.__m_tx_binding = self.__m_binding

        if not value.__eq__("None") and not value.__eq__(""):
            self.__m_tx_binding = value

    def set_tx_binding_by_hosts(self, ip_host: str, icc_host: str):
        WsiUtils.check_type(ip_host, str)
        WsiUtils.check_type(icc_host, str)
        new_binding_flag = 0

        if not icc_host.__eq__("None") and not icc_host.__eq__(""):
            self.__m_tx_binding = "|" + "wsi_icc:" + icc_host
            new_binding_flag = 1

        if not ip_host.__eq__("None") and not ip_host.__eq__(""):
            self.__m_tx_binding = self.__m_tx_binding + "|" + "wsi_tcp:" + ip_host
            self.__m_tx_binding = self.__m_tx_binding + "|" + "ncadg_ip_udp:" + ip_host
            self.__m_tx_binding = self.__m_tx_binding + "|" + "ncacn_ip_tcp:" + ip_host
            new_binding_flag = 1

        if new_binding_flag == 1:
            self.__m_tx_binding = self.__m_tx_binding + "|"
        else:
            self.__m_tx_binding = self.__m_binding

    """ Retrieve the Major Version property.
        @return Major Version value for the connection.
    """

    def get_major_version(self) -> int:
        return self.__m_major_version

    """ Update the Major Version property
        @param value     New value for the Major Version property
    """

    def set_major_version(self, value: int):
        WsiUtils.check_type(value, int)
        self.__m_major_version = value

    """ Retrieve the Minor Version property.
        @return Minor Version value for the connection.
    """

    def get_minor_version(self) -> int:
        return self.__m_minor_version

    """ Update the Minor Version property
        @param value     New value for the Minor Version property
    """

    def set_minor_version(self, value: int):
        WsiUtils.check_type(value, int)
        self.__m_minor_version = value

    """ Retrieve the Lease Timeout property.
        @ return lease timeout value for the connection.
    """

    def get_lease_timeout(self) -> int:
        return self.__m_lease_timeout

    """ Update the Lease Timeout property
        @ param value New value for the Lease Timeout property
    """

    def set_lease_timeout(self, value: int):
        WsiUtils.check_type(value, int)
        self.__m_lease_timeout = value

    """ Indicate if the NativeShell instance is to be local to this JVM or
        at a remote RMI server.
        @return true, if the JNI contact is to be in this JVM, and false, if not.
        @see #getHostName()
        @see #setHostName(String)
    """

    def is_local(self) -> bool:
        return (self.__m_ip_host_name is None) or (self.__m_ip_host_name.__len__() == 0) or (
            self.__m_ip_host_name.lower().__eq__("localhost"))

    """ Getter for property appName.
        @return Value of property appName.
    """

    def get_app_name(self) -> str:
        return self.__m_app_name

    """ Setter for property appName.
        @param appName New value of property appName.
    """

    def set_app_name(self, value: str):
        WsiUtils.check_type(value, str)
        self.__m_app_name = value

    """ Getter for property appUuid.
        @return Value of property appUuid.
    """

    def get_app_uuid(self) -> str:
        return self.__m_app_uuid

    """ Setter for property appUuid.
        @param appUuid New value of property appUuid.
    """

    def set_app_uuid(self, value: str):
        WsiUtils.check_type(value, str)
        self.__m_app_uuid = value

    """ Getter for property Domain.
        @return Value of property Domain.
    """

    def get_domain(self) -> str:
        return self.__m_domain

    """ Setter for property Domain.
        @param Domain New value of property Domain.
    """

    def set_domain(self, value):
        WsiUtils.check_type(value, str)
        self.__m_domain = value

    """ @return
    """

    def is_app_multithreaded(self) -> bool:
        return self.__m_is_app_multithreaded

    """ Return whether the server sharable is to be loaded into the current
        process space or not.
    """

    def is_transport(self) -> bool:
        return self.__m_is_transport

    """ @param value
        @throws IllegalArgumentException
    """

    def set_session_type_int(self, value: int):
        WsiUtils.check_type(value, int)
        if not value in [ServerConfig.NO_SESSION, ServerConfig.TX_SESSION, ServerConfig.LIFETIME_SESSION,
                         ServerConfig.TX_LIFETIME]:
            raise AttributeError("sessionType must be NO_SESSION, TX_SESSION, LIFETIME_SESSION or TX_LIFETIME")
        self.__m_session_type = value

    """ @param value
        @throws IllegalArgumentException
    """

    def set_session_type_str(self, value: str):
        WsiUtils.check_type(value, str)
        if value.lower().__eq__("no_session"):
            new_val = ServerConfig.NO_SESSION
        elif value.lower().__eq__("tx_session"):
            new_val = ServerConfig.TX_SESSION
        elif value.lower().__eq__("lifetime_session"):
            new_val = ServerConfig.LIFETIME_SESSION
        elif value.lower().__eq__("tx_lifetime"):
            new_val = ServerConfig.TX_LIFETIME
        else:
            raise AttributeError("sessionType must be NO_SESSION, TX_SESSION, LIFETIME_SESSION or TX_LIFETIME")
        self.__m_session_type = new_val

    """ @return
    """

    def get_session_type(self) -> int:
        return self.__m_session_type

    """ Custom string formatting method.
    """

    def to_string(self) -> str:
        return "ServerConfig: mBinding = " + str(self.__m_binding) + ", appName = " + str(self.__m_app_name) + ", sessionType = " + str(self.__m_session_type)

    """ Add a PropertyChangeListener to the listener list.
        @param l The listener to add.
    """
    # def add_property_change_listener(self, l):
    # property_support.add_property_change_listener(l)

    """ Removes a PropertyChangeListener from the listener list.
        @param l The listener to remove.
    """

    # def remove_property_change_listener(self, l):

    def get_tcp_ip_name(self) -> str:
        return self.__m_ip_host_name

    def set_tcp_ip_name(self, m_ip_host_name: str):
        WsiUtils.check_type(m_ip_host_name, str)
        self.__m_ip_host_name = m_ip_host_name

    def get_scs_node_name(self) -> str:
        return self.__m_icc_host_name

    def set_scs_node_name(self, m_icc_host_name: str):
        WsiUtils.check_type(m_icc_host_name, str)
        self.__m_icc_host_name = m_icc_host_name

    def get_tx_tcp_ip_name(self) -> str:
        return self.__m_tx_ip_host_name

    def set_tx_tcp_ip_name(self, m_tx_ip_host_name: str):
        WsiUtils.check_type(m_tx_ip_host_name, str)
        self.__m_tx_ip_host_name = m_tx_ip_host_name

    def get_tx_scs_node_name(self) -> str:
        return self.__m_tx_icc_host_name

    def set_tx_scs_node_name(self, m_tx_icc_host_name: str):
        WsiUtils.check_type(m_tx_icc_host_name, str)
        self.__m_tx_icc_host_name = m_tx_icc_host_name

    def __setattr__(self, name, value):
        WsiUtils.check_set_attr(self, name, value)
