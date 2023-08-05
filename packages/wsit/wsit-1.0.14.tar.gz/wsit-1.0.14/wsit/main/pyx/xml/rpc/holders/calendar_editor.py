from datetime import datetime
from wsit.main.pyx.xml.rpc.holders.calendar_holder import CalendarHolder
from wsit.main.pyx.xml.rpc.holders.holder_editor import HolderEditor


class CalendarEditor(HolderEditor):

    def __init__(self):
        super().__init__(datetime(1, 1, 1))

    def set_value(self, new_value):
        if isinstance(new_value, datetime):
            super().set_value(new_value)
        else:
            raise TypeError("value must be a datetime type")

    def set_as_text(self, new_value):
        try:
            if type(new_value) is str:
                super().set_value(datetime.strptime(new_value, CalendarHolder.date_format))
            else:
                raise TypeError("value must be string date in " + CalendarHolder.date_format + " format")
        except Exception as ex:
            raise Exception(ex.args[0])

    def get_as_text(self):
        return self.get_value().__format__(CalendarHolder.date_format)
