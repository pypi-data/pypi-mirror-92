import pytest

from wsit.main.com.vsi.wsi.wsi_xid_impl import WsiXidImpl
from wsit.main.com.vsi.wsi.xa_exception import XAException


class TestWsiXidImpl:
    def test_init_exception_1(self):
        xid_data = [0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x03, 0x00, 0x00, 0x00]
        with pytest.raises(XAException):
            wsi_xid = WsiXidImpl(xid_data)

    def test_init_exception_2(self):
        xid_data = [0x01, 0x00, 0x00, 0x00, 0x41, 0x00, 0x00, 0x00, 0x03, 0x00, 0x00, 0x00]
        with pytest.raises(XAException):
            wsi_xid = WsiXidImpl(xid_data)

    def test_init_exception_3(self):
        xid_data = [0x01, 0x00, 0x00, 0x00, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
        with pytest.raises(XAException):
            wsi_xid = WsiXidImpl(xid_data)

    def test_init_exception_4(self):
        xid_data = [0x01, 0x00, 0x00, 0x00, 0x02, 0x00, 0x00, 0x00, 0x41, 0x00, 0x00, 0x00]
        with pytest.raises(XAException):
            wsi_xid = WsiXidImpl(xid_data)

    def test_init(self):
        xid_data = [0x01, 0x00, 0x00, 0x00, 0x02, 0x00, 0x00, 0x00, 0x03, 0x00, 0x00, 0x00, 0x07, 0x07, 0x09, 0x09, 0x09]
        wsi_xid = WsiXidImpl(xid_data)
        tested_format_id = 1
        tested_gtrid = [0x07, 0x07]
        tested_bqual = [0x09, 0x09, 0x09]
        m_bqual = wsi_xid.get_branch_qualifier()
        m_gtrid = wsi_xid.get_global_transaction_id()

        assert wsi_xid.get_format_id() == tested_format_id
        for i in range(len(tested_gtrid)):
            assert tested_gtrid[i] == m_gtrid[i]
        for i in range(len(tested_bqual)):
            assert tested_bqual[i] == m_bqual[i]
