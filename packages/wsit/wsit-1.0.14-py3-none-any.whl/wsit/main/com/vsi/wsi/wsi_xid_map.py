from wsit.main.com.vsi.wsi.i_wsi_native_shell import IWsiNativeShell
from wsit.main.com.vsi.wsi.i_xa_resource import IXAResource
from wsit.main.com.vsi.wsi.i_xid import IXid
from wsit.main.com.vsi.wsi.wsi_utils import WsiUtils

"""
This singleton class holds a map of all active XIDs, and the WsiNativeShell instances that know about them.
"""


class WsiXIDMap:
    __my_this = None        # Reference to the single instance of this class
    __my_sema = "sema"      # This class variable is used as a semaphore to synchronize the original creation.
    """
    This variable is used as a semaphore to synchronize
    the forceDone method.  The synchronized keyword could not
    be used on the method directly, due to concerns of a deadlock
    condition caused by callback from XA_END to remove
    """
    __force_sema = "fSema"

    @staticmethod   # Return the singleton instance, creating it if necessary.
    def get_xid_map() -> 'WsiXIDMap':
        if WsiXIDMap.__my_this is None:
            WsiXIDMap.__my_this = WsiXIDMap()
        return WsiXIDMap.__my_this

    """
    Map of all known XIDs.  The key is the xid, and the value is a
    linked list containing all WsiNativeShell instances that have declared
    an interest in the XID.
    """
    __my_map = None

    def __init__(self):     # Create an instance of a XID map.
        self.__my_map = {}

    """
     Declare an interest in a particular XID.  If the XID was not
     previously known we create a base mapping entry.  If the shell
     instance was not previously interested in the XID we add a
     reference in the XID's attached list.
    """
    def add_if(self, xid: IXid, shell: IWsiNativeShell):
        WsiUtils.check_instance(xid, IXid)
        WsiUtils.check_instance(shell, IWsiNativeShell)
        linked_list = []
        if self.__my_map.__contains__(xid):
            """
            We have an entry in the map already.  Pick up the list of
            interested shell instances.  If the specified shell instance
            isn't in the list, add it.
            """
            linked_list = self.__my_map.get(xid)
            if shell not in linked_list:
                linked_list.append(shell)
                self.__my_map[xid] = linked_list
        else:
            """
            We do not have an entry in the list with this XID.  Create the
            simplest one -- just the XID and a list containing the
            specified shell instance.
            """
            linked_list.append(shell)
            self.__my_map[xid] = linked_list

    def remove(self, xid: IXid, shell: IWsiNativeShell):
        WsiUtils.check_instance(xid, IXid)
        WsiUtils.check_instance(shell, IWsiNativeShell)
        linked_list = self.__my_map.get(xid)
        if linked_list is not None:
            linked_list.remove(shell)
            if not linked_list:
                del self.__my_map[xid]

    """
    Force all currently interested parties in this XID to declare their threads as terminated.
    This method provides the base support to force all shell instances
    to terminate their suspended XID sessiosn.  These cover two important cases:
    
    1) A system exception arrives after a xa_end with TMSUSPEND.  WLS will
    send an xa_rollback without first issuing xa_end with a terminal
    flag, such as TMSUCCESS or TMFAIL.
    
    2) A transaction that spans several instances will typically issue
    xa_end calls with TMSUSPEND for all but the last thread.  This is
    legal, but leaves various servers attached with no way to detach
    them.
    """
    def force_done(self, xid: IXid):
        WsiUtils.check_instance(xid, IXid)
        s_list = self.__my_map.get(xid)
        if s_list is not None:
            work_list = self.get_shell_list(xid)
            if work_list is not None:
                """
                We have the XID in our map.  Make a copy of the list of
                interest shell instances, and then tell each to terminate their sessions.
                """
                for xashell in work_list:
                    xashell.end(xid, IXAResource.TMSUCCESS)

    def get_shell_list(self, xid: IXid) -> list:
        WsiUtils.check_instance(xid, IXid)
        if self.__my_map.__contains__(xid):
            """
            We have the XID in our map.  Make a copy of the list of
            interest shell instances, and then tell each to terminate their sessions.
            """
            return self.__my_map.get(xid)
        else:
            return None

    """
    Custom formatting routine.  This will display the contents of the
    full map -- formatting the XID map and its attached shell instances.
    Returns formatted display of the map contents.
    """
    def __str__(self):
        format_str = "com.hp.wsi.WsiXIDMap contents:\n"
        if len(self.__my_map) == 0:
            format_str += "\t-- empty --\n"
        else:
            for xid in self.__my_map.keys():
                linked_list = self.__my_map[xid]
                format_str += "    xid = " + str(xid) + "\n\tvalues = {"
                for shell in linked_list:
                    format_str += "\n        " + str(shell)
                format_str += "\n    }\n"
        return format_str

    def __setattr__(self, name, value):
        WsiUtils.check_set_attr(self, name, value)
