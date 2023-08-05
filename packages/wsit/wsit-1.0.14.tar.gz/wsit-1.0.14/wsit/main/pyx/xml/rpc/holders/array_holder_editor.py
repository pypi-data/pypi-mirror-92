from wsit.main.pyx.xml.rpc.holders.array_holder import ArrayHolder
from wsit.main.pyx.xml.rpc.holders.holder_editor import HolderEditor


class ArrayHolderEditor(HolderEditor):

    def __init__(self):
        super().__init__(ArrayHolder())

    def set_value(self, new_value):
        if isinstance(new_value, ArrayHolder):
            super().set_value(new_value)
        else:
            raise TypeError("value must be an ArrayHolder type")

    def set_as_text(self, new_value):
        raise ValueError("ArrayHolder can not have a value set on it")
