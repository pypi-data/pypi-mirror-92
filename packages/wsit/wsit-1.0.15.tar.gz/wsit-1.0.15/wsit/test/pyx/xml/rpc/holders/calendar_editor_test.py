import pytest
from wsit.main.pyx.xml.rpc.holders.calendar_editor import CalendarEditor
from wsit.test.pyx.xml.rpc.holders.calendar_holder_test import TestCalendarHolder


class TestCalendarEditor:
    def test_init(self):
        calendar_editor = CalendarEditor()
        assert calendar_editor.get_value() is not None

    def test_private_field(self):
        calendar_editor = CalendarEditor()
        with pytest.raises(AttributeError):
            calendar_editor.value = 123

    def test_set_value(self):
        calendar_editor = CalendarEditor()
        for tested_value in TestCalendarHolder.valid_values:
            calendar_editor.set_value(tested_value)
            assert tested_value == calendar_editor.get_value()

    def test_set_value_exception(self):
        calendar_editor = CalendarEditor()
        for tested_value in TestCalendarHolder.exception_values + TestCalendarHolder.exception_text_values:
            with pytest.raises(Exception):
                calendar_editor.set_value(tested_value)

    def test_set_as_text(self):
        calendar_editor = CalendarEditor()
        for tested_value in TestCalendarHolder.valid_text_values:
            calendar_editor.set_as_text(tested_value)
            assert tested_value.__eq__(calendar_editor.get_as_text())

    def test_set_as_text_exception(self):
        calendar_editor = CalendarEditor()
        for tested_value in TestCalendarHolder.exception_values + TestCalendarHolder.exception_text_values:
            with pytest.raises(Exception):
                calendar_editor.set_as_text(tested_value)
