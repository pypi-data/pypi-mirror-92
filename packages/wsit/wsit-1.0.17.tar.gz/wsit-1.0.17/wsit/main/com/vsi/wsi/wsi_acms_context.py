# This class allows the client application to provide WSIT the context
# in which to run ACMS tasks.  The attributes available for setting
# are Selection String & Application Name(not currently used).
# On return from the ACMS Task call, this context object will
# contain the ACMS Extended Status from the call.
from wsit.main.com.vsi.wsi.wsi_utils import WsiUtils


class WsiAcmsContext:
    __selection_string = None
    __extended_status = None
    __application_name = None

    # Creates a new instance of WsiAcmsContext using a specified selection string or without it
    def __init__(self):
        pass

    @classmethod
    def init_by_sel_str(cls, new_value: str) -> 'WsiAcmsContext':
        wsi_acms_context = cls()
        wsi_acms_context.set_sel_string(new_value)
        return wsi_acms_context

    # Sets the selection string within this object
    # @param selectionString selection string to set within this object
    def set_sel_string(self, new_value: str):
        WsiUtils.check_type(new_value, str)
        self.__selection_string = new_value

    # Returns the selection string set within this object
    # @return selection string as currently set within this object
    def get_sel_string(self) -> str:
        return self.__selection_string

    # Sets the extended status within this object
    # This call should not be used by a client.  It is used by the generated
    # PyBean to set this value one return from an ACMS Task call.
    # @param extendedStatus the extended status returned from an ACMS Task call.
    def set_ext_status(self, new_value: str):
        WsiUtils.check_type(new_value, str)
        self.__extended_status = new_value

    # Returns the extended status set within this object
    # This is always set on the return from an ACMS Task call.
    # @return the current extended status
    def get_ext_status(self) -> str:
        return self.__extended_status

    # Sets the dynamic application name within this object.
    # (*This is not currently used.*)
    #
    # @param applicationName dynamic application name to set within this object
    def set_app_name(self, new_value: str):
        WsiUtils.check_type(new_value, str)
        self.__application_name = new_value

    # Returns the dynamic application name currently set within this object.
    # (*This is not currently used.*)
    #
    # @return dynamic application name as currently set within this object
    def get_app_name(self) -> str:
        return self.__application_name

    # Returns a string representation of the internal value.
    def __str__(self) -> str:
        return "Selection String = " + self.__selection_string + "\n" + "Extended Status = " + self.__extended_status \
               + "\n" + "Application Name = " + self.__application_name

    def __setattr__(self, name, value):
        WsiUtils.check_set_attr(self, name, value)
