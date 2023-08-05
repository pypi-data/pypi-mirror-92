"""
 *  Maintain a local cache of known Xids.
 *
 *  <p>
 *  This is used by a JNIShell instance to maintain the set of XIDs that have
 *  active or suspended branches on its attached server.
 *
 *  <p>
 *  Note that as it expects the caller to be synchronized itself, this class
 *  performs no synchronization of its own.
"""


from wsit.main.com.vsi.wsi.i_xid import IXid
from wsit.main.com.vsi.wsi.wsi_utils import WsiUtils


class WsiXidCache:

    """
     *  Hold the list of known Xids.  This list is expected to normally be
     *  quite small (empty, or 1).  Therefore, even though most access will
     *  require a search of the list, it does not make sense to use a HashMap.
    """
    __my_xids = []

    def __init__(self):
        self.__my_xids.clear()

    """
         *  Add a Xid to the known list, unless it is already there.
         *
         *  @param  xid     XID to add to the list.
    """
    def add_if(self, xid: IXid):
        if not self.has_xid(xid):
            self.__my_xids.append(xid)

    """
     *  Remove the specified XID from our local cache, if it is present.
     *
     *  @param  xid     XID to remove from our cache
    """
    def drop_if(self, xid: IXid):
        # Look up the exact XID in the list.
        if self.has_xid(xid):
            self.__my_xids.remove(xid)

    """
     *  Determine if the XID is present in the local cache.
     *
     *  @param  xid     XID to look for in the cache.
     *  @returns true, if the XID is matched; false if not.
    """
    def has_xid(self, xid: IXid):
        WsiUtils.check_instance(xid, IXid)
        try:
            self.__my_xids.index(xid)
            return True
        except ValueError:
            # .index(object) throws the ValueError in case of object is not in the list
            return False

    """
     *  Are any XIDs currently held in the cache?
     *
     *  @returns true, if there are XIDs in the cache; false if not.
    """
    def is_empty(self) -> bool:
        return len(self.__my_xids) == 0

    def __setattr__(self, name, value):
        WsiUtils.check_set_attr(self, name, value)
