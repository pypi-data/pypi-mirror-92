from wsit.main.pyx.xml.rpc.holders.holder import Holder


class CharHolder(Holder):
    
    def __init__(self, new_value='\0'):
        self.set(new_value)

    def set(self, new_value):
        if isinstance(new_value, str) and new_value.__len__() == 1:
            super().set(new_value)
        else:
            raise TypeError("value must be one symbol string")

    def __eq__(self, obj):
        if isinstance(obj, CharHolder):
            return self.get() == obj.get()
        return False
