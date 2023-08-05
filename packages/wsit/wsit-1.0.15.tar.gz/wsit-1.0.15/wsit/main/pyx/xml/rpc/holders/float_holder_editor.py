from wsit.main.pyx.xml.rpc.holders.holder_editor import HolderEditor
from wsit.main.pyx.xml.rpc.holders.float_holder import FloatHolder


class FloatHolderEditor(HolderEditor):

    def __init__(self):
        super().__init__(FloatHolder())

    def set_value(self, new_value):
        if isinstance(new_value, FloatHolder):
            super().set_value(new_value)
        else:
            raise TypeError("value must be a FloatHolder type")

    def set_as_text(self, new_value):
        if type(new_value) is str:
            try:
                self.get_value().set(float(new_value))
            except Exception as ex:
                raise ValueError(ex.args[0])
        else:
            raise TypeError("type must be a string representation of a float type")
