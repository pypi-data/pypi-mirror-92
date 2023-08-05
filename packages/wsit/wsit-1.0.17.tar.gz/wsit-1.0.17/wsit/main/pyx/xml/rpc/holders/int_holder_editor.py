from wsit.main.pyx.xml.rpc.holders.holder_editor import HolderEditor
from wsit.main.pyx.xml.rpc.holders.int_holder import IntHolder


class IntHolderEditor(HolderEditor):

    def __init__(self):
        super().__init__(IntHolder())

    def set_value(self, new_value):
        if isinstance(new_value, IntHolder):
            super().set_value(new_value)
        else:
            raise TypeError("value must be an IntHolder type")

    def set_as_text(self, new_value):
        if type(new_value) is str:
            try:
                super().get_value().set(int(new_value))
            except Exception as ex:
                raise Exception(ex.args[0])
        else:
            raise TypeError("value must be a string representation of an int")
