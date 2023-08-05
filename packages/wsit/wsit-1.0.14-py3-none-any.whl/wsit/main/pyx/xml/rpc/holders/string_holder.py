from wsit.main.pyx.xml.rpc.holders.holder import Holder


class StringHolder(Holder):

    def __init__(self, new_value=None):
        self.set(new_value)

    def set(self, new_value):
        if isinstance(new_value, str) or new_value is None:
            super().set(new_value)
        else:
            raise TypeError("value must be a string type")

    def __eq__(self, obj):
        if isinstance(obj, StringHolder):
            return self.get() == obj.get()
        return False
