from wsit.main.com.vsi.wsi.wsi_utils import WsiUtils
from wsit.main.pyx.xml.rpc.holders.holder_editor import HolderEditor
from wsit.main.pyx.xml.rpc.holders.structure_holder import StructureHolder


class StructureHolderEditor(HolderEditor):
    def __init__(self):
        super().__init__(StructureHolder())

    def set_value(self, new_value):
        WsiUtils.check_instance(new_value, StructureHolder)
        super().set_value(new_value)

    def set_as_text(self, new_value):
        raise TypeError("StructureHolder can not have a value set on it")
