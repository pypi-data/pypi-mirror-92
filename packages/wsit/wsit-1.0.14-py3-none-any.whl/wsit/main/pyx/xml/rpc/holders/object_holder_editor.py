from wsit.main.pyx.xml.rpc.holders.holder_editor import HolderEditor
from wsit.main.pyx.xml.rpc.holders.object_holder import ObjectHolder


class ObjectHolderEditor(HolderEditor):

    def __init__(self):
        super().__init__(ObjectHolder())

    def set_value(self, new_value):
        if isinstance(new_value, ObjectHolder):
            super().set_value(new_value)
        else:
            raise Exception("Value must be an ObjectHolder type")

    def set_as_text(self, new_value):
        raise Exception("ObjectHolder can not have a value set on it")
