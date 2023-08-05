import pytest
from wsit.main.pyx.xml.rpc.holders.array_holder import ArrayHolder
from wsit.main.pyx.xml.rpc.holders.array_holder_editor import ArrayHolderEditor
from wsit.test.pyx.xml.rpc.holders.array_holder_test import TestArrayHolder


class TestArrayHolderEditor:
    def test_init(self):
        array_holder_editor = ArrayHolderEditor()
        array_holder = array_holder_editor.get_value()
        assert array_holder.get() is None

    def test_private_field(self):
        array_holder_editor = ArrayHolderEditor()
        with pytest.raises(AttributeError):
            array_holder_editor.value = 123

    def test_set_value(self):
        array_holder_editor = ArrayHolderEditor()
        for tested_value in TestArrayHolder.valid_values:
            array_holder = ArrayHolder(tested_value)
            array_holder_editor.set_value(array_holder)
            assert array_holder == array_holder_editor.get_value()

    def test_set_value_exception(self):
        array_holder_editor = ArrayHolderEditor()
        for tested_value in TestArrayHolder.valid_values:
            with pytest.raises(Exception):
                array_holder_editor.set_value(tested_value)

    def test_set_as_text_exception(self):
        array_holder_editor = ArrayHolderEditor()
        for tested_value in TestArrayHolder.valid_values:
            with pytest.raises(Exception):
                array_holder_editor.set_as_text(str(tested_value))
                array_holder_editor.set_as_text(tested_value)

    def test_get_as_text(self):
        array_holder_editor = ArrayHolderEditor()
        for tested_value in TestArrayHolder.valid_values:
            array_holder_editor.set_value(ArrayHolder(tested_value))
            assert str(tested_value).__eq__(array_holder_editor.get_as_text())
