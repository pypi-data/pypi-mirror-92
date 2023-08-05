from wsit.main.pyx.xml.rpc.holders.holder_editor import HolderEditor
from wsit.main.pyx.xml.rpc.holders.char_holder import CharHolder


class CharHolderEditor(HolderEditor):

    def __init__(self):
        super().__init__(CharHolder())

    def set_value(self, new_value):
        if isinstance(new_value, CharHolder):
            super().set_value(new_value)
        else:
            raise TypeError("value must be a CharHolder type")

    def set_as_text(self, new_value):
        if isinstance(new_value, str) and new_value.__len__() > 0:
            super().get_value().set(new_value[0])
        else:
            raise ValueError("value must be a non empty string")
