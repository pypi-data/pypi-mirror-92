from wsit.main.pyx.xml.rpc.holders.holder_editor import HolderEditor


class BigIntegerEditor(HolderEditor):

    def __init__(self):
        super().__init__(0)

    def set_value(self, new_value):
        if type(new_value) is int:
            super().set_value(new_value)
        else:
            raise TypeError("value must be an int type")

    def set_as_text(self, new_value):
        try:
            if type(new_value) is str:
                super().set_value(int(new_value))
            else:
                raise TypeError("value must be a string representation of an int")
        except Exception as ex:
            raise ValueError(ex.args[0])
