import numpy as np

from wsit.main.pyx.xml.rpc.holders.holder import Holder


class DoubleHolder(Holder):

    def __init__(self, new_value=0.0):
        self.set(new_value)

    def set(self, new_value):
        if type(new_value) in [int, float]:
            super().set(float(new_value))
        else:
            raise TypeError("value must be double, float or int")

    def __eq__(self, obj):
        if isinstance(obj, DoubleHolder):
            return np.allclose(self.get(), obj.get())
        return False
