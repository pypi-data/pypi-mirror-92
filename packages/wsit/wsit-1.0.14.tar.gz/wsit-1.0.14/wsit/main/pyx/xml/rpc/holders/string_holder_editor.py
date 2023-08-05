from wsit.main.pyx.xml.rpc.holders.holder_editor import HolderEditor
from wsit.main.pyx.xml.rpc.holders.string_holder import StringHolder


class StringHolderEditor(HolderEditor):

    def __init__(self):
        super().__init__(StringHolder())

    def set_value(self, new_value):
        if isinstance(new_value, StringHolder):
            super().set_value(new_value)
        else:
            raise TypeError("value must be a StringHolder type")

    def set_as_text(self, new_value):
        if type(new_value) is str:
            super().get_value().set(new_value)
        else:
            raise TypeError("value must be a string type")
