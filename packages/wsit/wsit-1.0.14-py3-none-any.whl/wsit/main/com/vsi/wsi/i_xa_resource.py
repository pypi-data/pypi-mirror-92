from typing import List

from wsit.main.com.vsi.wsi.i_xid import IXid
from wsit.main.com.vsi.wsi.wsi_utils import WsiUtils


class IXAResource:
    TMENDRSCAN = 8388608
    TMFAIL = 536870912
    TMJOIN = 2097152
    TMNOFLAGS = 0
    TMONEPHASE = 1073741824
    TMRESUME = 134217728
    TMSTARTRSCAN = 16777216
    TMSUCCESS = 67108864
    TMSUSPEND = 33554432
    XA_RDONLY = 3
    XA_OK = 0

    def commit(self, xid: IXid, b: bool):
        WsiUtils.check_instance(xid, IXid)
        WsiUtils.check_type(b, bool)

    def end(self, xid: IXid, i: int):
        WsiUtils.check_instance(xid, IXid)
        WsiUtils.check_type(i, int)

    def forget(self, xid: IXid):
        WsiUtils.check_instance(xid, IXid)

    def get_transaction_timeout(self) -> int:
        return 0

    def is_same_rm(self, xa_resource: 'IXAResource') -> bool:
        WsiUtils.check_instance(xa_resource, IXAResource)
        return False

    def prepare(self, xid: IXid) -> int:
        WsiUtils.check_instance(xid, IXid)
        return 0

    def recover(self, i: int) -> list:
        WsiUtils.check_type(i, int)
        list_ixid = List[IXid]
        return list_ixid

    def rollback(self, xid: IXid):
        WsiUtils.check_instance(xid, IXid)

    def set_transaction_timeout(self, i: int) -> bool:
        WsiUtils.check_type(i, int)
        return False

    def start(self, xid: IXid, i: int):
        WsiUtils.check_instance(xid, IXid)
        WsiUtils.check_type(i, int)
