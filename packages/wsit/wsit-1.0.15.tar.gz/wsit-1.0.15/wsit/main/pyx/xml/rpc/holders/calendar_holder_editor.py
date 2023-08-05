from datetime import datetime
from wsit.main.pyx.xml.rpc.holders.calendar_holder import CalendarHolder
from wsit.main.pyx.xml.rpc.holders.holder_editor import HolderEditor


class CalendarHolderEditor(HolderEditor):
    def __init__(self):
        super().__init__(CalendarHolder())

    def set_value(self, new_value):
        if isinstance(new_value, CalendarHolder):
            super().set_value(new_value)
        else:
            raise TypeError("value must be a CalendarHolder type")

    def set_as_text(self, new_value):
        try:
            if type(new_value) is str:
                self.get_value().set(datetime.strptime(new_value, CalendarHolder.date_format))
            else:
                raise TypeError("value must be string date in " + CalendarHolder.date_format + " format")
        except Exception as ex:
            raise Exception(ex.args[0])
