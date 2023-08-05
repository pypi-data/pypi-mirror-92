from interface import implements

from wsit.main.pyx.xml.rpc.holders.iproperty_editor import IPropertyEditor


class HolderEditor(implements(IPropertyEditor)):

    __holder_value = None

    def __init__(self, new_value=None):
        self.__holder_value = new_value

    def __setattr__(self, name, value):
        if not hasattr(self, name):
            raise AttributeError('''Can't set attribute "{0}"'''.format(name))
        object.__setattr__(self, name, value)

    def set_value(self, new_value):
        self.__holder_value = new_value

    def get_value(self):
        return self.__holder_value

    def set_as_text(self, new_value):
        self.__holder_value = str(new_value)

    def get_as_text(self):
        return str(self.__holder_value)
