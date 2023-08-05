from wsit.main.com.vsi.wsi.wsi_utils import WsiUtils


class IXid:
    MAXGTRIDSIZE = 64
    MAXBQUALSIZE = 64

    def get_format_id(self):
        pass

    def get_global_transaction(self):
        pass

    def get_branch_qualifier(self):
        pass

    def __setattr__(self, name, value):
        WsiUtils.check_set_attr(self, name, value)
