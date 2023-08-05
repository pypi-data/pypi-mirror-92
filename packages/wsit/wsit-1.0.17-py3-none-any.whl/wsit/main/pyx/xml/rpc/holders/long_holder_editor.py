from wsit.main.pyx.xml.rpc.holders.holder_editor import HolderEditor
from wsit.main.pyx.xml.rpc.holders.long_holder import LongHolder


class LongHolderEditor(HolderEditor):

    def __init__(self):
        super().__init__(LongHolder())

    def set_value(self, new_value):
        if isinstance(new_value, LongHolder):
            super().set_value(new_value)
        else:
            raise TypeError("value must be a LongHolder type")

    def set_as_text(self, new_value):
        if type(new_value) is str:
            try:
                super().get_value().set(int(new_value))
            except Exception as ex:
                raise Exception(ex.args[0])
        else:
            raise TypeError("value must be a string representation of a long")
