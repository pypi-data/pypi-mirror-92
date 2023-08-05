from datetime import datetime

import pytest

from wsit.main.pyx.xml.rpc.holders.calendar_holder import CalendarHolder


class TestCalendarHolder:

    exception_values = ["value", 'string', 'a', "b", '', "", True, False, "True", "False", "0", "1", '0', '1', 234.890,
                        -7389457908.39485797, '124.9090798', '-0.126155', "-803485.9457897", "4564690846908.4059680890",
                        "485739857", "-4573875937", None, "None", 'None', 273698276, -798576, 0, 1]

    valid_values = [datetime.min, datetime.max, datetime(1986, 7, 17), datetime(2001, 5, 28), datetime(1, 1, 1)]

    valid_text_values = ["2015-05-15 06:39:00", "2017-04-23 11:00:00"]

    exception_text_values = ["99.99.99 99:99", "1.1.1 1:1", "-12.12.12 00:00", "12.-12.12 00:00", "12.12.-12 00:00",
                             "25.09.2010 00:00", "30.02.13 00:00", "25.18.18 00:00", "11.18.18 -01:00"]

    def test_init(self):
        calendar_holder = CalendarHolder()
        date_time = datetime(1, 1, 1)
        assert date_time == calendar_holder.get()

    def test_private_field(self):
        calendar_holder = CalendarHolder()
        with pytest.raises(AttributeError):
            calendar_holder.value = 123

    def test_init_param(self):
        for tested_value in TestCalendarHolder.valid_values:
            calendar_holder = CalendarHolder(tested_value)
            assert tested_value == calendar_holder.get()

    def test_init_exception(self):
        for tested_value in TestCalendarHolder.exception_values:
            with pytest.raises(TypeError):
                calendar_holder = CalendarHolder(tested_value)

    def test_to_string(self):
        for tested_value in TestCalendarHolder.valid_values:
            calendar_holder = CalendarHolder(tested_value)
            assert tested_value.__eq__(calendar_holder.__str__())

    def test_equals(self):
        date_time_1 = datetime(7, 7, 7)
        date_time_2 = datetime(7, 7, 9)
        calendar_holder_1 = CalendarHolder(date_time_1)
        calendar_holder_2 = CalendarHolder(date_time_1)

        assert calendar_holder_1.__eq__(None) is False
        assert calendar_holder_1.__eq__(123) is False
        assert calendar_holder_1.__eq__(calendar_holder_1) is True
        assert calendar_holder_1.__eq__(calendar_holder_2) is True
        calendar_holder_2.set(date_time_2)
        assert calendar_holder_1.__eq__(calendar_holder_2) is False
