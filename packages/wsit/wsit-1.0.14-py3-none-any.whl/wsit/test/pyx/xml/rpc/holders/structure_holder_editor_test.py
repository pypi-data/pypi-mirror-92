import pytest

from wsit.main.com.vsi.wsi.wsi_structure import WsiStructure
from wsit.main.pyx.xml.rpc.holders.structure_holder import StructureHolder
from wsit.main.pyx.xml.rpc.holders.structure_holder_editor import StructureHolderEditor


class TestStructureHolderEditor:
    def test_init(self):
        structure_holder_editor = StructureHolderEditor()
        structure_holder = structure_holder_editor.get_value()
        assert structure_holder.get() is None

    def test_set_value(self):
        structure_holder_editor = StructureHolderEditor()
        wsi_structure = WsiStructure()
        structure_holder = StructureHolder.init_by_wsi_structure(wsi_structure)
        structure_holder_editor.set_value(structure_holder)
        assert structure_holder_editor.get_value() == structure_holder

    def test_set_as_text(self):
        tested_value = "test"
        structure_holder_editor = StructureHolderEditor()
        with pytest.raises(Exception):
            structure_holder_editor.set_as_text(tested_value)

    def test_get_as_text(self):
        structure_holder_editor = StructureHolderEditor()
        structure_holder = StructureHolder()
        structure_holder_editor.set_value(structure_holder)
        assert structure_holder_editor.get_as_text().__eq__("None")

    def test_private_field(self):
        byte_holder_editor = StructureHolderEditor()
        with pytest.raises(AttributeError):
            byte_holder_editor.value = 123
