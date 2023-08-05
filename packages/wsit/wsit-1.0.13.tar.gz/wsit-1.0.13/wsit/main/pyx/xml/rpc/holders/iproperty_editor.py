from interface import Interface


class IPropertyEditor(Interface):

    def __init__(self):
        pass

    def set_value(self, new_value):
        pass

    def get_value(self):
        pass

    def set_as_text(self, new_value):
        pass

    def get_as_text(self):
        pass
