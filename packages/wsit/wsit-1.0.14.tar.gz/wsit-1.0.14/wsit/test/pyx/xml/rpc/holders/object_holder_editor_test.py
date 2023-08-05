import pytest
from wsit.main.pyx.xml.rpc.holders.object_holder import ObjectHolder
from wsit.main.pyx.xml.rpc.holders.object_holder_editor import ObjectHolderEditor
from wsit.test.pyx.xml.rpc.holders.object_holder_test import TestObjectHolder


class TestObjectHolderEditor:
    def test_init(self):
        object_holder_editor = ObjectHolderEditor()
        object_holder = object_holder_editor.get_value()
        assert object_holder.get() is None

    def test_private_field(self):
        object_holder_editor = ObjectHolderEditor()
        with pytest.raises(AttributeError):
            object_holder_editor.value = 123

    def test_set_value(self):
        object_holder_editor = ObjectHolderEditor()
        for tested_value in TestObjectHolder.valid_values:
            object_holder_editor.set_value(ObjectHolder(tested_value))
            object_holder = object_holder_editor.get_value()
            assert tested_value == object_holder.get()

    def test_set_value_exception(self):
        object_holder_editor = ObjectHolderEditor()
        for tested_value in TestObjectHolder.valid_values:
            with pytest.raises(Exception):
                object_holder_editor.set_value(tested_value)

    def test_set_as_text_exception(self):
        object_holder_editor = ObjectHolderEditor()
        for tested_value in TestObjectHolder.valid_values:
            with pytest.raises(Exception):
                object_holder_editor.set_as_text(tested_value)

    def test_get_as_text(self):
        object_holder_editor = ObjectHolderEditor()
        for tested_value in TestObjectHolder.valid_values:
            object_holder_editor.set_value(ObjectHolder(tested_value))
            assert tested_value.__str__().__eq__(object_holder_editor.get_as_text())
