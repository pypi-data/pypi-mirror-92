from wsit.main.pyx.xml.rpc.holders.holder import Holder


class UIntHolder(Holder):
    MIN_VALUE = 0
    MAX_VALUE = 4294967295

    def __init__(self, new_value=0):  # constructor with param
        self.set(new_value)

    def set(self, new_value):
        if isinstance(new_value, int) and type(new_value) is not bool:
            if self.MIN_VALUE <= new_value <= self.MAX_VALUE:
                super().set(new_value)
            else:
                raise ValueError("Value too small or too large: " + new_value.__str__())
        else:
            raise TypeError("value must be an unsigned int type")

    def __eq__(self, obj):
        if isinstance(obj, UIntHolder):
            return self.get() == obj.get()
        return False
