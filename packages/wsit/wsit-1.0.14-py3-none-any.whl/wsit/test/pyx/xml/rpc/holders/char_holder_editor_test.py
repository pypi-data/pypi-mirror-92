import pytest

from wsit.main.pyx.xml.rpc.holders.char_holder import CharHolder
from wsit.main.pyx.xml.rpc.holders.char_holder_editor import CharHolderEditor
from wsit.test.pyx.xml.rpc.holders.char_holder_test import TestCharHolder


class TestCharHolderEditor:
    def test_init(self):
        char_holder_editor = CharHolderEditor()
        assert char_holder_editor.get_value().get() == '\0'

    def test_private_field(self):
        char_holder_editor = CharHolderEditor()
        with pytest.raises(AttributeError):
            char_holder_editor.value = 123

    def test_set_value(self):
        char_holder_editor = CharHolderEditor()
        for tested_value in TestCharHolder.valid_values:
            char_holder = CharHolder(tested_value)
            char_holder_editor.set_value(char_holder)
            assert tested_value == char_holder_editor.get_value().get()

    def test_set_value_exception(self):
        char_holder_editor = CharHolderEditor()
        for tested_value in TestCharHolder.exception_values:
            with pytest.raises(Exception):
                char_holder_editor.set_value(tested_value)

    def test_set_as_text(self):
        char_holder_editor = CharHolderEditor()
        for tested_value in TestCharHolder.valid_text_values + TestCharHolder.valid_values:
            char_holder_editor.set_as_text(tested_value)
            assert tested_value[0] == char_holder_editor.get_as_text()

    def test_set_as_text_exception(self):
        char_holder_editor = CharHolderEditor()
        for tested_value in TestCharHolder.exception_text_values:
            with pytest.raises(Exception):
                char_holder_editor.set_as_text(tested_value)
