import pytest

from wsit.main.com.vsi.wsi.wsi_rtl_version import WsiRtlVersion


class TestWsiRtlVersion:
    def test_init(self):
        tested_value = "V1.1-8"
        assert WsiRtlVersion.get_version() == tested_value

    def test_private_field(self):
        wsi_rtl_version = WsiRtlVersion()
        with pytest.raises(AttributeError):
            wsi_rtl_version.value = 123
