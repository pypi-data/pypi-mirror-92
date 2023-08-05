import pytest

from wsit.main.pyx.xml.rpc.holders.calendar_holder import CalendarHolder
from wsit.main.pyx.xml.rpc.holders.calendar_holder_editor import CalendarHolderEditor
from wsit.test.pyx.xml.rpc.holders.calendar_holder_test import TestCalendarHolder


class TestCalendarHolderEditor:
    def test_init(self):
        calendar_holder_editor = CalendarHolderEditor()
        calendar_holder = CalendarHolder()
        assert calendar_holder.get() == calendar_holder_editor.get_value().get()

    def test_private_field(self):
        calendar_holder_editor = CalendarHolderEditor()
        with pytest.raises(AttributeError):
            calendar_holder_editor.value = 123

    def test_set_value(self):
        calendar_holder_editor = CalendarHolderEditor()
        for tested_value in TestCalendarHolder.valid_values:
            calendar_holder = CalendarHolder(tested_value)
            calendar_holder_editor.set_value(calendar_holder)
            assert calendar_holder == calendar_holder_editor.get_value()

    def test_set_value_exception(self):
        calendar_holder_editor = CalendarHolderEditor()
        for tested_value in TestCalendarHolder.exception_values:
            with pytest.raises(Exception):
                calendar_holder_editor.set_value(tested_value)

    def test_set_as_text(self):
        calendar_holder_editor = CalendarHolderEditor()
        for tested_value in TestCalendarHolder.valid_text_values:
            calendar_holder_editor.set_as_text(tested_value)
            assert tested_value == calendar_holder_editor.get_as_text()

    def test_set_as_text_exception(self):
        calendar_holder_editor = CalendarHolderEditor()
        for tested_value in TestCalendarHolder.exception_values + TestCalendarHolder.exception_text_values:
            with pytest.raises(Exception):
                calendar_holder_editor.set_as_text(tested_value)
