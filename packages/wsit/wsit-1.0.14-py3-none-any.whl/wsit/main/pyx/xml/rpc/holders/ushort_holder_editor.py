from wsit.main.pyx.xml.rpc.holders.holder_editor import HolderEditor
from wsit.main.pyx.xml.rpc.holders.ushort_holder import UShortHolder


class UShortHolderEditor(HolderEditor):

    def __init__(self):
        super().__init__(UShortHolder())

    def set_value(self, new_value):
        if isinstance(new_value, UShortHolder):
            super().set_value(new_value)
        else:
            raise TypeError("value must be an UShortHolder type")

    def set_as_text(self, new_value):
        if type(new_value) is str:
            try:
                super().get_value().set(int(new_value))
            except Exception as ex:
                raise Exception(ex.args[0])
        else:
            raise TypeError("value must be a string representation of an unsigned short")
