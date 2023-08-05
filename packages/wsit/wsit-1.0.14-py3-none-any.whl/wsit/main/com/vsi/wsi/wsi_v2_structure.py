from typing import List
from wsit.main.com.vsi.wsi.wsi_structure import WsiStructure


class WsiV2Structure:
    def __init__(self):
        self.struct_buffer = None
        self.struct_alignment = 0
        self.wsi_structure = None

    @classmethod
    def init_by_struct_size_alignment_byte_array(cls, struct_size: int, alignment: int,
                                                 bytes: List[int]) -> 'WsiV2Structure':
        from wsit.main.com.vsi.wsi.wsi_utils import WsiUtils, IntegerTypes
        WsiUtils.check_type(struct_size, int)
        WsiUtils.check_type(alignment, int)
        WsiUtils.check_list_type_of_intervals(bytes, IntegerTypes.BYTE)
        wsi_v2_structure = cls()
        wsi_v2_structure.wsi_structure = WsiStructure()
        wsi_v2_structure.wsi_structure.struct_size = struct_size
        wsi_v2_structure.wsi_structure.struct_alignment = alignment
        from wsit.main.com.vsi.wsi.wsi_buffer import WsiBuffer
        wsi_v2_structure.wsi_structure.set_buffer(WsiBuffer.init_by_buffer(bytes), 0)
        return wsi_v2_structure

    def retrieve_wsi_structure(self) -> 'WsiStructure':
        return self.wsi_structure
