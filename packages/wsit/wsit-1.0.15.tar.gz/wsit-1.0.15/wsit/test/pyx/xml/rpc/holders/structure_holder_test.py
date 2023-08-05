import pytest

from wsit.main.com.vsi.wsi.wsi_structure import WsiStructure
from wsit.main.pyx.xml.rpc.holders.structure_holder import StructureHolder


class TestStructureHolder:
    def test_init(self):
        structure_holder = StructureHolder()
        assert structure_holder.get() is None

        wsi_structure = WsiStructure()
        structure_holder = StructureHolder.init_by_wsi_structure(wsi_structure)
        assert structure_holder.get().__eq__(wsi_structure)

    def test_to_string(self):
        structure_holder = StructureHolder()
        tested_value = "None"
        assert str(structure_holder).__eq__(tested_value)

    def test_equals(self):
        structure_holder = StructureHolder()
        structure_holder_same = StructureHolder()
        structure_holder_other = StructureHolder()

        assert structure_holder.__eq__(None) is False
        assert structure_holder.__eq__(int(5)) is False
        assert structure_holder.__eq__(structure_holder) is True
        assert structure_holder.__eq__(structure_holder_same) is True
        structure_holder_other.set(WsiStructure())
        assert structure_holder.__eq__(structure_holder_other) is False

    def test_private_field(self):
        byte_holder = StructureHolder()
        with pytest.raises(AttributeError):
            byte_holder.value = 123
