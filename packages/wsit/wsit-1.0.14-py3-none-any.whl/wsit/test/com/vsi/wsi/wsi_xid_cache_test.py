import pytest

from wsit.main.com.vsi.wsi.i_xid import IXid
from wsit.main.com.vsi.wsi.wsi_xid_cache import WsiXidCache


class TestWsiXidCache:

    def test_init(self):
        wsi_xid_cache = WsiXidCache()
        assert wsi_xid_cache.is_empty() is True

    def test_add_if(self):
        wsi_xid_cache = WsiXidCache()
        ixid1 = IXid()
        ixid2 = IXid()
        assert wsi_xid_cache.has_xid(ixid1) is False
        assert wsi_xid_cache.has_xid(ixid2) is False
        assert wsi_xid_cache.is_empty() is True

        wsi_xid_cache.add_if(ixid1)
        wsi_xid_cache.add_if(ixid2)
        assert wsi_xid_cache.has_xid(ixid1) is True
        assert wsi_xid_cache.has_xid(ixid2) is True
        assert wsi_xid_cache.is_empty() is False

    def test_drop_if(self):
        wsi_xid_cache = WsiXidCache()
        ixid1 = IXid()
        ixid2 = IXid()
        assert wsi_xid_cache.is_empty() is True

        wsi_xid_cache.add_if(ixid1)
        wsi_xid_cache.add_if(ixid2)
        assert wsi_xid_cache.is_empty() is False
        assert wsi_xid_cache.has_xid(ixid1) is True
        assert wsi_xid_cache.has_xid(ixid2) is True

        wsi_xid_cache.drop_if(ixid1)
        assert wsi_xid_cache.has_xid(ixid1) is False
        assert wsi_xid_cache.has_xid(ixid2) is True
        assert wsi_xid_cache.is_empty() is False

        wsi_xid_cache.drop_if(ixid1)  # try to drop non-existing Xid
        assert wsi_xid_cache.has_xid(ixid1) is False
        assert wsi_xid_cache.is_empty() is False

        wsi_xid_cache.drop_if(ixid2)
        assert wsi_xid_cache.has_xid(ixid1) is False
        assert wsi_xid_cache.has_xid(ixid2) is False
        assert wsi_xid_cache.is_empty() is True

    def test_private_field(self):
        wsi_xid_cache = WsiXidCache()
        with pytest.raises(AttributeError):
            wsi_xid_cache.value = 123
