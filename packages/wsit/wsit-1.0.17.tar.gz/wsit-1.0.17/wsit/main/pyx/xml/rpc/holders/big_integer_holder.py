from wsit.main.pyx.xml.rpc.holders.holder import Holder


class BigIntegerHolder(Holder):

    def __init__(self, new_value=0):
        self.set(new_value)

    def set(self, new_value):
        if type(new_value) is int:
            super().set(new_value)
        else:
            raise TypeError("value must be an int type")

    def __eq__(self, obj):
        if isinstance(obj, BigIntegerHolder):
            return self.get() == obj.get()
        return False
