import pytest
from wsit.main.pyx.xml.rpc.holders.int_holder_editor import IntHolderEditor
from wsit.main.pyx.xml.rpc.holders.int_holder import IntHolder
from wsit.test.pyx.xml.rpc.holders.int_holder_test import TestIntHolder


class TestIntHolderEditor:

    def test_init(self):
        int_holder_editor = IntHolderEditor()
        assert int_holder_editor.get_value().get() == 0

    def test_private_field(self):
        int_holder_editor = IntHolderEditor()
        with pytest.raises(AttributeError):
            int_holder_editor.value = 123

    def test_set_value(self):
        int_holder_editor = IntHolderEditor()
        for tested_value in TestIntHolder.valid_values:
            int_holder = IntHolder(tested_value)
            int_holder_editor.set_value(int_holder)
            assert int_holder.get() == int_holder_editor.get_value().get()

    def test_set_value_exception(self):
        int_holder_editor = IntHolderEditor()
        # Only IntHolder type allowed
        for tested_value in TestIntHolder.exception_values + TestIntHolder.valid_values:
            with pytest.raises(TypeError):
                int_holder_editor.set_value(tested_value)

    def test_set_as_text(self):
        int_holder_editor = IntHolderEditor()
        for tested_value in TestIntHolder.valid_values:
            int_holder_editor.set_as_text(tested_value.__str__())
            assert int_holder_editor.get_as_text().__eq__(tested_value.__str__())

    def test_set_as_text_exception(self):
        int_holder_editor = IntHolderEditor()
        for tested_value in TestIntHolder.exception_text_values:
            with pytest.raises(Exception):
                int_holder_editor.set_as_text(tested_value)
