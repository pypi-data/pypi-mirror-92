from wsit.main.pyx.xml.rpc.holders.holder_editor import HolderEditor
from wsit.main.pyx.xml.rpc.holders.byte_holder import ByteHolder


class ByteHolderEditor(HolderEditor):

    def __init__(self):
        super().__init__(ByteHolder())

    def set_value(self, new_value):
        if isinstance(new_value, ByteHolder):
            super().set_value(new_value)
        else:
            raise TypeError("value must be a ByteHolder type")

    def set_as_text(self, new_value):
        if type(new_value) is str:
            try:
                self.get_value().set(int(new_value))
            except Exception as ex:
                raise ValueError(ex.args[0])
        else:
            raise TypeError("value must be a string representation of a byte")
