import pytest
from wsit.main.pyx.xml.rpc.holders.ushort_holder_editor import UShortHolderEditor
from wsit.main.pyx.xml.rpc.holders.ushort_holder import UShortHolder
from wsit.test.pyx.xml.rpc.holders.ushort_holder_test import TestUShortHolder


class TestUShortHolderEditor:

    def test_init(self):
        ushort_holder_editor = UShortHolderEditor()
        assert ushort_holder_editor.get_value().get() == 0

    def test_private_field(self):
        ushort_holder_editor = UShortHolderEditor()
        with pytest.raises(AttributeError):
            ushort_holder_editor.value = 123

    def test_set_value(self):
        ushort_holder_editor = UShortHolderEditor()
        for tested_value in TestUShortHolder.valid_values:
            ushort_holder = UShortHolder(tested_value)
            ushort_holder_editor.set_value(ushort_holder)
            assert ushort_holder.get() == ushort_holder_editor.get_value().get()

    def test_set_value_exception(self):
        ushort_holder_editor = UShortHolderEditor()
        for tested_value in TestUShortHolder.exception_values:
            with pytest.raises(Exception):
                ushort_holder_editor.set_value(tested_value)

    def test_set_as_text(self):
        ushort_holder_editor = UShortHolderEditor()
        for tested_value in TestUShortHolder.valid_values:
            ushort_holder_editor.set_as_text(tested_value.__str__())
            assert ushort_holder_editor.get_as_text().__eq__(tested_value.__str__())

    def test_set_as_text_exception(self):
        ushort_holder_editor = UShortHolderEditor()
        for tested_value in TestUShortHolder.exception_text_values:
            with pytest.raises(Exception):
                ushort_holder_editor.set_as_text(tested_value)
