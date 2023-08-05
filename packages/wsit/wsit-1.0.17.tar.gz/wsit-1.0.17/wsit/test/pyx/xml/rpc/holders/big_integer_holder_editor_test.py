import pytest

from wsit.main.pyx.xml.rpc.holders.big_integer_holder import BigIntegerHolder
from wsit.main.pyx.xml.rpc.holders.big_integer_holder_editor import BigIntegerHolderEditor
from wsit.test.pyx.xml.rpc.holders.big_integer_holder_test import TestBigIntegerHolder


class TestBigIntegerHolderEditor:
    def test_init(self):
        big_integer_holder_editor = BigIntegerHolderEditor()
        big_integer_holder = big_integer_holder_editor.get_value()
        assert big_integer_holder.get() == 0

    def test_private_field(self):
        big_integer_holder_editor = BigIntegerHolderEditor()
        with pytest.raises(AttributeError):
            big_integer_holder_editor.value = 123

    def test_set_value(self):
        big_integer_holder_editor = BigIntegerHolderEditor()
        for tested_value in TestBigIntegerHolder.valid_values:
            big_integer_holder_editor.set_value(BigIntegerHolder(tested_value))
            big_integer_holder = big_integer_holder_editor.get_value()
            assert tested_value == big_integer_holder.get()

    def test_set_value_exception(self):
        big_integer_holder = BigIntegerHolder()
        for tested_value in TestBigIntegerHolder.exception_values:
            with pytest.raises(Exception):
                big_integer_holder.set_value(tested_value)

    def test_set_as_text(self):
        big_integer_holder_editor = BigIntegerHolderEditor()
        for tested_value in TestBigIntegerHolder.valid_values:
            big_integer_holder_editor.set_as_text(str(tested_value))
            assert str(tested_value).__eq__(big_integer_holder_editor.get_as_text())

    def test_set_as_text_exception(self):
        big_integer_holder_editor = BigIntegerHolderEditor()
        for tested_value in TestBigIntegerHolder.exception_text_values:
            with pytest.raises(Exception):
                big_integer_holder_editor.set_as_text(tested_value)
