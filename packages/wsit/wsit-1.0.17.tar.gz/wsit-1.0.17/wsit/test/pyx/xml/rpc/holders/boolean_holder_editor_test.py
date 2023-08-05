import pytest
from wsit.main.pyx.xml.rpc.holders.boolean_holder_editor import BooleanHolderEditor
from wsit.main.pyx.xml.rpc.holders.boolean_holder import BooleanHolder
from wsit.test.pyx.xml.rpc.holders.boolean_holder_test import TestBooleanHolder


class TestBooleanHolderEditor:

    def test_init(self):
        boolean_holder_editor = BooleanHolderEditor()
        boolean_holder = BooleanHolder()
        assert boolean_holder.get() == boolean_holder_editor.get_value().get()

    def test_private_field(self):
        boolean_holder_editor = BooleanHolderEditor()
        with pytest.raises(AttributeError):
            boolean_holder_editor.value = 123

    def test_set_value(self):
        boolean_holder_editor = BooleanHolderEditor()
        for tested_value in TestBooleanHolder.valid_values:
            boolean_holder = BooleanHolder(tested_value)
            boolean_holder_editor.set_value(boolean_holder)
            assert boolean_holder.get() == boolean_holder_editor.get_value().get()

    def test_set_value_exception(self):
        boolean_holder_editor = BooleanHolderEditor()
        for tested_value in TestBooleanHolder.exception_values:
            with pytest.raises(Exception):
                boolean_holder_editor.set_value(tested_value)

    def test_set_as_text(self):
        boolean_holder_editor = BooleanHolderEditor()
        for tested_value in TestBooleanHolder.valid_text_values:
            boolean_holder_editor.set_as_text(tested_value)
            assert tested_value.lower().__eq__(boolean_holder_editor.get_as_text().lower())

    def test_set_as_text_exception(self):
        boolean_holder_editor = BooleanHolderEditor()
        for tested_value in TestBooleanHolder.exception_text_values:
            with pytest.raises(Exception):
                boolean_holder_editor.set_as_text(tested_value)
