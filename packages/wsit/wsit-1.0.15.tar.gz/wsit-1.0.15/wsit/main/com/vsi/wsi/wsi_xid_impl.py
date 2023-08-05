from typing import List

from wsit.main.com.vsi.wsi.i_xid import IXid
from wsit.main.com.vsi.wsi.wsi_utils import WsiUtils
from wsit.main.com.vsi.wsi.wsi_utils import IntegerTypes
from wsit.main.com.vsi.wsi.xa_exception import XAException


class WsiXidImpl:

    # Creates a new XidImpl instance, and initializes it with a byte array
    # that contains an XA compliant XID.
    # The XID buffer format is defined by the X/Open XA specification.
    # The layout in the data buffer is (starting at the first byte):
    # 4 bytes:    XID format ID
    # 4 bytes:    Size of the GTRID value
    # 4 bytes:    Size of the BQUAL value
    # GTRID length:   GTRID value
    # BQUAL length:   BQUAL value

    def __init__(self, xid_data: List[int]):
        WsiUtils.check_list_type_of_intervals(xid_data, IntegerTypes.BYTE)

        # Use the standard message decoder to pick up the three longwords
        # that form the fixed part of th XID.
        from wsit.main.com.vsi.wsi.wsi_buffer import WsiBuffer
        dec = WsiBuffer()
        dec.set_buffer_by_buffer(xid_data)

        self.__m_format_id = dec.get_int()
        self.__m_gtrid = []
        self.__m_bqual = []
        self.gtrid_len = dec.get_int()
        self.bqual_len = dec.get_int()

        # Validate the GTRID and BQUAL sizes before continuing.
        if self.gtrid_len <= 0 or self.gtrid_len > IXid.MAXGTRIDSIZE or self.bqual_len <= 0 or self.bqual_len > IXid.MAXGTRIDSIZE:
            raise XAException(XAException.XAER_INVAL)

        # All valid.  Now copy all the gtid and bqual values ouf of the byte array into our new instance.
        self.__m_gtrid = [0] * self.gtrid_len
        self.__m_bqual = [0] * self.bqual_len

        i_index = 12 + self.gtrid_len
        self.__m_gtrid[:self.gtrid_len] = xid_data[12: i_index]
        self.__m_bqual[:self.bqual_len] = xid_data[i_index: i_index+self.bqual_len]

    # Retrieve the bqual, or branch qualifier, value
    # @return branch qualifier value
    def get_branch_qualifier(self) -> List[int]:
        return self.__m_bqual

    # Retrieve the format ID code for this XID.
    # @return format ID code
    def get_format_id(self) -> int:
        return self.__m_format_id

    # Retrieve the gtrid, or global transaction ID.
    # @return gtrid value for this XID.
    def get_global_transaction_id(self) -> List[int]:
        return self.__m_gtrid
