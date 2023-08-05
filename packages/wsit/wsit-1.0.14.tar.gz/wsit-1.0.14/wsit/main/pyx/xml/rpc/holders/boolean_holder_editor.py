from wsit.main.pyx.xml.rpc.holders.holder_editor import HolderEditor
from wsit.main.pyx.xml.rpc.holders.boolean_holder import BooleanHolder


class BooleanHolderEditor(HolderEditor):

    def __init__(self):
        super().__init__(BooleanHolder())

    def set_value(self, new_value):
        if isinstance(new_value, BooleanHolder):
            super().set_value(new_value)
        else:
            raise TypeError("value must be a BooleanHolder type")

    def set_as_text(self, new_value):
        if type(new_value) is str:
            if new_value.lower() == "true":
                self.get_value().set(True)
            elif new_value.lower() == "false":
                self.get_value().set(False)
            else:
                raise ValueError("value must be True or False")
        else:
            raise TypeError("value must be a string representation of a bool type")
