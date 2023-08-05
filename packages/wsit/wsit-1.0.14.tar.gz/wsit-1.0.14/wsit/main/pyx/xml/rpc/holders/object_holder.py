from wsit.main.pyx.xml.rpc.holders.holder import Holder


class ObjectHolder(Holder):

    def __init__(self, new_value=None):
        super().__init__(new_value)

    def __eq__(self, obj):
        if isinstance(obj, ObjectHolder):
            return self.get() == obj.get()
        return False
