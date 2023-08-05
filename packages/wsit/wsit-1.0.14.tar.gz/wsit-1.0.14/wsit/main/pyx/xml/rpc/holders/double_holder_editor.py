from wsit.main.pyx.xml.rpc.holders.holder_editor import HolderEditor
from wsit.main.pyx.xml.rpc.holders.double_holder import DoubleHolder


class DoubleHolderEditor(HolderEditor):

    def __init__(self):
        super().__init__(DoubleHolder())

    def set_value(self, new_value):
        if isinstance(new_value, DoubleHolder):
            super().set_value(new_value)
        else:
            raise TypeError("value must be a DoubleHolder type")

    def set_as_text(self, new_value):
        if type(new_value) is str:
            try:
                self.get_value().set(float(new_value))
            except Exception as ex:
                raise ValueError(ex.args[0])
        else:
            raise TypeError("type must be a string representation of a double")
