from datetime import datetime, date
from wsit.main.pyx.xml.rpc.holders.holder import Holder


class CalendarHolder(Holder):
    date_format = '%Y-%m-%d %H:%M:%S'

    def __init__(self, new_value=datetime(1, 1, 1)):
        self.set(new_value)

    def set(self, new_value):
        if isinstance(new_value, date):
            super().set(new_value)
        else:
            raise TypeError("value must be a datetime")

    def __str__(self):
        return self.get().__format__(self.date_format)

    def __eq__(self, obj):
        if isinstance(obj, CalendarHolder):
            return self.get() == obj.get()
        return False
