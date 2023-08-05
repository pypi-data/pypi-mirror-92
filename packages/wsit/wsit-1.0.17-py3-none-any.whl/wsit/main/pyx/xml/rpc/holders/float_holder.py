from wsit.main.pyx.xml.rpc.holders.holder import Holder
import numpy as np


class FloatHolder(Holder):

    def __init__(self, new_value=0.0):
        self.set(new_value)

    def set(self, new_value):
        if type(new_value) in [int, float, np.float32]:
            super().set(np.float32(new_value))
        else:
            raise TypeError("value must be a float or an int type")

    def __eq__(self, obj):
        if isinstance(obj, FloatHolder):
            return np.allclose(self.get(), obj.get())
        return False
