from wsit.main.com.vsi.wsi.wsi_utils import WsiUtils


class WsiException(Exception):
    __detail = None
    # privately stored exception codes.
    __m_exc_code = 0
    __m_vms_code = 0
    __m_facility = 0
    __m_severity = 0
    # privately used flags & masks
    __WSIsM_SEVERITY = 0x7  # Severity Mask
    __WSIsM_FAC_NO = 0xFFF0000  # Facility Number Mask
    __WSIsM_MSG_NO = 0xFFF8  # Message Number Mask

    # public severity flags & masks
    # This identifies the exception or error as having a warning level
    WSIsK_WARNING = 0  # Warning
    # This identifies the exception or error as having a success level
    WSIsK_SUCCESS = 1  # Successful completion
    # This identifies the exception or error as having an error level
    WSIsK_ERROR = 2  # Error
    # This identifies the exception or error as having an informational(success) level
    WSIsK_INFO = 3  # Information
    # This identifies the exception or error as having a severe error level
    WSIsK_SEVERE = 4  # Severe error

    # public facility flags & masks
    # This identifies the exception or error as originating within the interprocess communication layer.
    WSIsK_FAC_IPC = 1  # IPC
    # This identifies the exception or error as originating within the RTL in the pybean process.
    WSIsK_FAC_RTL = 2  # RTL
    # This identifies the exception or error as originating within the wsi$manager process.
    WSIsK_FAC_MGR = 3  # Wsi$Manager
    # This identifies the exception or error as originating within the server process.
    WSIsK_FAC_SVR = 4  # Server

    def __init(self):
        super().__init__()

    @classmethod
    def init_from_er_msg(cls, er_message: str) -> 'WsiException':
        WsiUtils.check_type(er_message, str)
        wsi_exception = cls()
        wsi_exception.args = [er_message]
        return wsi_exception

    @classmethod
    def init_from_er_msg_except(cls, ex: Exception, er_message: str) -> 'WsiException':
        WsiUtils.check_instance(ex, Exception)
        WsiUtils.check_type(er_message, str)
        wsi_exception = cls()
        wsi_exception.args = [er_message]
        wsi_exception.__detail = ex
        return wsi_exception

    @classmethod
    def init_from_except(cls, ex: Exception) -> 'WsiException':
        WsiUtils.check_instance(ex, Exception)
        wsi_exception = cls()
        wsi_exception.__detail = ex
        return wsi_exception

    @classmethod
    def init_from_er_msg_ex_code_vms_code(cls, er_message: str, in_exc_code: int,
                                          in_vms_code: int) -> 'WsiException':
        WsiUtils.check_type(er_message, str)
        WsiUtils.check_type(in_exc_code, int)
        WsiUtils.check_type(in_vms_code, int)
        wsi_exception = cls()
        wsi_exception.args = [er_message]
        wsi_exception.__m_exc_code = in_exc_code
        wsi_exception.__m_vms_code = in_vms_code
        return wsi_exception

    @classmethod
    def init_from_er_msg_ex_code_vms_code_severity_facility(cls, er_message: str, in_exc_code: int, in_vms_code: int,
                                                            in_severity: int, in_facility: int) -> 'WsiException':
        WsiUtils.check_type(er_message, str)
        WsiUtils.check_type(in_exc_code, int)
        WsiUtils.check_type(in_vms_code, int)
        WsiUtils.check_type(in_severity, int)
        WsiUtils.check_type(in_facility, int)
        wsi_exception = cls()
        wsi_exception.args = [er_message]
        wsi_exception.__m_exc_code = in_exc_code
        wsi_exception.__m_vms_code = in_vms_code
        wsi_exception.__m_severity = in_severity
        wsi_exception.__m_facility = in_facility
        return wsi_exception

    @classmethod
    def init_from_wsi_exception(cls, wsi_ex: 'WsiException') -> 'WsiException':
        WsiUtils.check_instance(wsi_ex, WsiException)
        wsi_exception = cls()
        wsi_exception.args = [wsi_ex.get_message()]
        wsi_exception.__m_exc_code = wsi_ex.get_status()
        wsi_exception.__m_vms_code = wsi_ex.get_vms_status()
        wsi_exception.__m_severity = wsi_ex.get_severity()
        wsi_exception.__m_facility = wsi_ex.get_facility()
        return wsi_exception

    # Return the Internal exception code if one exists2
    #
    # @return internal exception code
    def get_status(self):
        return self.__m_exc_code

    # Return the OpenVMS exception status if one exists
    #
    # @return original OpenVMS error status
    def get_vms_status(self):
        return self.__m_vms_code

    # Return the Severity level if available
    #
    # @return severity level of this exception.  (Refer to the WSI$K_# status level definitions.)
    def get_severity(self):
        return self.__m_severity

    # Return the Facility Code if available
    #
    # @return facility that originated this exception.  (Refer to the WSI$K_FAC_* definitions.)
    def get_facility(self):
        return self.__m_facility

    # Return a flag indicating if the connection to the server process is still valid.
    # This can be used by a client to determine if it needs to close the connection
    # and reestablish a fresh connection to the server.
    def is_connection_valid(self):
        valid_flag = True
        # These statements make up the 'rules' by which we determine
        # if a connection is valid or not
        if self.__m_facility == self.WSIsK_FAC_MGR or (self.__m_facility == self.WSIsK_FAC_IPC and self.__m_severity == self.WSIsK_SEVERE):
            valid_flag = False
        return valid_flag

    def get_message(self):
        return self.args[0]

    def get_detail(self):
        return self.__detail

    def __setattr__(self, name, value):
        WsiUtils.check_set_attr(self, name, value)
