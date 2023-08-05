from interface import implements
from wsit.main.pyx.xml.rpc.holders.iholder import IHolder


class Holder(implements(IHolder)):

    __value = None

    def __init__(self, new_value=None):
        self.__value = new_value

    def __setattr__(self, name, value):
        if not hasattr(self, name):
            raise AttributeError('''Can't set attribute "{0}"'''.format(name))
        object.__setattr__(self, name, value)

    def set(self, new_value):
        self.__value = new_value

    def get(self):
        return self.__value

    def __str__(self):
        return str(self.__value)
