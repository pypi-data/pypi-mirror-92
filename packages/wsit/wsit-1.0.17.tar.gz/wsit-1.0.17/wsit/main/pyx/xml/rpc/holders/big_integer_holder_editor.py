from wsit.main.pyx.xml.rpc.holders.big_integer_holder import BigIntegerHolder
from wsit.main.pyx.xml.rpc.holders.holder_editor import HolderEditor


class BigIntegerHolderEditor(HolderEditor):

    def __init__(self):
        super().__init__(BigIntegerHolder())

    def set_value(self, new_value):
        if isinstance(new_value, BigIntegerHolder):
            super().set_value(new_value)
        else:
            raise ValueError("value must be a BigIntegerHolder type")

    def set_as_text(self, new_value):
        try:
            if type(new_value) is str:
                self.get_value().set(int(new_value))
            else:
                raise TypeError("value must be a string representation of an int")
        except Exception as ex:
            raise ValueError(ex.args[0])
