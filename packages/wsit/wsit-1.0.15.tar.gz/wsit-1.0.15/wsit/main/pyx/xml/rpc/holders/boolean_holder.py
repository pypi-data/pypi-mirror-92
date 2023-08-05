from wsit.main.pyx.xml.rpc.holders.holder import Holder


class BooleanHolder(Holder):

    def __init__(self, new_value=False):
        self.set(new_value)

    def set(self, new_value):
        if isinstance(new_value, bool):
            super().set(new_value)
        else:
            raise TypeError("value must be a bool type")

    def __eq__(self, obj):
        if isinstance(obj, BooleanHolder):
            return self.get() == obj.get()
        return False
