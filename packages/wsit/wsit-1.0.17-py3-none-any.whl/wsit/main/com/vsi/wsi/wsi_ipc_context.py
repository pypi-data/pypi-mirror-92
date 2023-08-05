"""
**
 *      This class allows the client to specify properties that effect
 *      instantiation & session control for out-of-process connections.
 *      Every WSIT generated PyBean optionally takes one of these
 *      objects.  The properties that can be specified within this
 *      context object include:
 *              Session Lifetime Specification, and an associated Lease Timeout
 *
 * Session control is used to specify the duration/type of connection between
 * the  (Python) and the Server Wrapper when out-of-proc communication is used.
 *
 * The following are the valid values for Session Control:
 *
 *   public  static final int        NO_SESSION = 0;
 *          (**NO_SESSION maintains no open session between PyBean & Server)
 *
 *   public  static final int        TX_SESSION = 1;
 *          (**TX_SESSION maintains session for duration of ACMS and/or OpenVMS Login only)
 *
 *   public  static final int        LIFETIME_SESSION = 2;
 *          (LIFETIME_SESSION maintains an open session for the duration of the PyBean)
 *
 *   To improve performance in the NO_SESSION & TX_SESSION cases,
 *   a lease timeout value (in seconds) can be specified to keep often
 *   used connections readily available.  These connections only need to be
 *   reestablished if left idle for longer than the timeout period.
 *
 */
"""
from wsit.main.com.vsi.wsi.server_config import ServerConfig
from wsit.main.com.vsi.wsi.wsi_utils import WsiUtils


class WsiIpcContext(ServerConfig):
    """
    /**
     * Session control value stating that no connection should be maintained to the
     * server between calls.
     */
     """
    NO_SESSION = 0
    """
    /**
     * Session control value stating that a connection should be maintained to the
     * server between calls only as long as there is an ACMS sign in session or
     * OpenVMS login session currently active.
     */
     """
    TX_SESSION = 1
    """
    /**
     * Session control value stating that a connection should be maintained to the
     * server between calls, and until the pybean itself goes away.
     */
    """
    LIFETIME_SESSION = 2
    """
    /**
     * Creates a new instance of WsiIpcContext with default values
     */
    """

    def __init__(self):
        super().__init__()

    """
    /**
     * Creates a new instance of WsiIpcContext with a specified session type and lease timeout.
     *
     *  @param stype     New value for Session Control Type property
     *  @param lease     New value for the Lease Timeout property
     *
     * @exception IllegalArgumentException if an unknown session type is specified.
     */
     """

    @classmethod
    def init_by_stype_lease(cls, stype: int, lease: int) -> 'WsiIpcContext':
        wsi_ipc_context = cls()
        wsi_ipc_context.set_session_type_int(stype)
        wsi_ipc_context.set_lease_timeout(lease)
        return wsi_ipc_context

    """
    /**
     * Creates a new instance of WsiIpcContext with a specified session type and lease timeout.
     *
     *  @param stype     New value for Session Control Type property
     *  @param lease     New value for the Lease Timeout property
     *
     * @exception IllegalArgumentException if an unknown session type is specified.
     */
     """

    @classmethod
    def init_by_sesstype_lease(cls, sesstype: str, lease: int) -> 'WsiIpcContext':
        WsiUtils.check_type(sesstype, str)
        wsi_ipc_context = cls()
        stype = WsiIpcContext.LIFETIME_SESSION
        if sesstype.upper().__eq__("NO_SESSION"):
            stype = WsiIpcContext.NO_SESSION
        if sesstype.upper().__eq__("TX_SESSION"):
            stype = WsiIpcContext.TX_SESSION
        wsi_ipc_context.set_session_type_int(stype)
        wsi_ipc_context.set_lease_timeout(lease)
        return wsi_ipc_context

    """
    /**
     * Set the session type for this connection.
     *
     * @param value     Session type of value NO_SESSION, TX_SESSION, or LIFETME_SESSION
     *
     * @exception IllegalArgumentException if an unknown session type is specified.
     */
     """

    def set_session_type_int(self, value: int):
        super().set_session_type_int(value)

    """
    /**
     * Return the Session type for this connection
     *
     * @return session type value for the connection.
     */
    """

    def get_session_type(self) -> int:
        return super().get_session_type()

    """
    /**
     * Sets the Lease Timeout property
     *
     *  @param value     New value for the Lease Timeout property
     */
    """

    def set_lease_timeout(self, value: int):
        super().set_lease_timeout(value)

    """
    /**
     * Returns the Lease Timeout property.
     *
     *  @return lease timeout value for the connection.
     */
    """

    def get_lease_timeout(self) -> int:
        return super().get_lease_timeout()
