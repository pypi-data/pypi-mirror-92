from wsit.main.com.vsi.wsi.wsi_structure import WsiStructure
from wsit.main.com.vsi.wsi.wsi_utils import WsiUtils
from wsit.main.pyx.xml.rpc.holders.holder import Holder


class StructureHolder(Holder):
    def __init__(self):
        self.set(None)

    @classmethod
    def init_by_wsi_structure(cls, new_value: 'WsiStructure'):
        WsiUtils.check_instance(new_value, WsiStructure)
        structure_holder = cls()
        structure_holder.set(new_value)
        return structure_holder

    def __eq__(self, obj):
        if isinstance(obj, StructureHolder):
            return self.get() == obj.get()
        return False
