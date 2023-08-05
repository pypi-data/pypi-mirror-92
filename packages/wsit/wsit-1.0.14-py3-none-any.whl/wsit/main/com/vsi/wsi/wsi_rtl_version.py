from wsit.main.com.vsi.wsi.wsi_utils import WsiUtils


class WsiRtlVersion:
    __wsi_rtl_version = "V1.1-8"

    @staticmethod
    def get_version():
        return WsiRtlVersion.__wsi_rtl_version

    def __setattr__(self, name, value):
        WsiUtils.check_set_attr(self, name, value)
