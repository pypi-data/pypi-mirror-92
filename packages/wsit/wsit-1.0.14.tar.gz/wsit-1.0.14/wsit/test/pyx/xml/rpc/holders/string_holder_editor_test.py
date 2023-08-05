import pytest

from wsit.main.pyx.xml.rpc.holders.string_holder_editor import StringHolderEditor
from wsit.main.pyx.xml.rpc.holders.string_holder import StringHolder
from wsit.test.pyx.xml.rpc.holders.string_holder_test import TestStringHolder


class TestStringHolderEditor:

    def test_init(self):
        string_holder_editor = StringHolderEditor()
        assert string_holder_editor.get_value().get() is None

    def test_private_field(self):
        string_holder_editor = StringHolderEditor()
        with pytest.raises(AttributeError):
            string_holder_editor.value = 123

    def test_set_value(self):
        string_holder_editor = StringHolderEditor()
        for tested_value in TestStringHolder.valid_values:
            string_holder = StringHolder(tested_value)
            string_holder_editor.set_value(string_holder)
            assert string_holder_editor.get_value().get() == tested_value

    def test_set_value_exception(self):
        string_holder_editor = StringHolderEditor()
        # Only StringHolder type is allowed
        for tested_value in TestStringHolder.exception_values + TestStringHolder.valid_values:
            with pytest.raises(Exception):
                string_holder_editor.set_value(tested_value)

    def test_set_as_text(self):
        string_holder_editor = StringHolderEditor()
        for tested_value in TestStringHolder.valid_values:
            string_holder_editor.set_as_text(tested_value)
            assert string_holder_editor.get_as_text().__eq__(tested_value)

    def test_set_as_text_exception(self):
        string_holder_editor = StringHolderEditor()
        for tested_value in TestStringHolder.exception_values:
            with pytest.raises(Exception):
                string_holder_editor.set_as_text(tested_value)
