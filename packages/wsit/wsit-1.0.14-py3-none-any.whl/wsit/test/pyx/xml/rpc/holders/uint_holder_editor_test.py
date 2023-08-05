import pytest
from wsit.main.pyx.xml.rpc.holders.uint_holder_editor import UIntHolderEditor
from wsit.main.pyx.xml.rpc.holders.uint_holder import UIntHolder
from wsit.test.pyx.xml.rpc.holders.uint_holder_test import TestUIntHolder


class TestUIntHolderEditor:
    
    def test_init(self):
        uint_holder_editor = UIntHolderEditor()
        assert uint_holder_editor.get_value().get() == 0

    def test_private_field(self):
        uint_holder_editor = UIntHolderEditor()
        with pytest.raises(AttributeError):
            uint_holder_editor.value = 123

    def test_set_value(self):
        uint_holder_editor = UIntHolderEditor()
        for tested_value in TestUIntHolder.valid_values:
            int_holder = UIntHolder(tested_value)
            uint_holder_editor.set_value(int_holder)
            assert int_holder.get() == uint_holder_editor.get_value().get()

    def test_set_value_exception(self):
        uint_holder_editor = UIntHolderEditor()
        # Only UIntHolder type allowed
        for tested_value in TestUIntHolder.exception_values + TestUIntHolder.valid_values:
            with pytest.raises(TypeError):
                uint_holder_editor.set_value(tested_value)

    def test_set_as_text(self):
        uint_holder_editor = UIntHolderEditor()
        for tested_value in TestUIntHolder.valid_values:
            uint_holder_editor.set_as_text(tested_value.__str__())
            assert uint_holder_editor.get_as_text().__eq__(tested_value.__str__())

    def test_set_as_text_exception(self):
        uint_holder_editor = UIntHolderEditor()
        for tested_value in TestUIntHolder.exception_text_values:
            with pytest.raises(Exception):
                uint_holder_editor.set_as_text(tested_value)
