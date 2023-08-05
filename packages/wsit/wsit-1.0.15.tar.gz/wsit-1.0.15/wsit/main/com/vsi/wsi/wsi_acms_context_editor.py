from wsit.main.com.vsi.wsi.wsi_acms_context import WsiAcmsContext
from wsit.main.com.vsi.wsi.wsi_utils import WsiUtils
from wsit.main.pyx.xml.rpc.holders.holder_editor import HolderEditor


class WsiAcmsContextEditor(HolderEditor):
    null = "null"

    def __init__(self):
        super().__init__(WsiAcmsContext())

    def set_value(self, new_value):
        WsiUtils.check_instance(new_value, WsiAcmsContext)
        super().set_value(new_value)

    def set_as_text(self, new_value):
        WsiUtils.check_type(new_value, str)
        if new_value.lower().__eq__(self.null):
            super().__init__(WsiAcmsContext())
        else:
            raise ValueError("WsiAcmsContext can not have a string value set on it")
