from wsit.main.pyx.xml.rpc.holders.object_holder import ObjectHolder


class ArrayHolder(ObjectHolder):

    def __init__(self, new_value=None):
        self.__check_new_value_types(new_value)
        super().__init__(new_value)

    def set(self, new_value):
        self.__check_new_value_types(new_value)
        super().set(new_value)

    def __check_new_value_types(self, new_value):
        if new_value is not None:
            if isinstance(new_value, list):
                first_type = None
                for i in range(len(new_value)):
                    if new_value[i] is None:
                        continue
                    current_type = type(new_value[i])
                    if first_type is None:
                        first_type = current_type
                        continue
                    elif current_type is not first_type:
                        raise TypeError("All elements in the list must be the same type")
            else:
                raise TypeError("Parameter must be a list")

    def __eq__(self, obj):
        if isinstance(obj, ArrayHolder):
            return self.get() == obj.get()
        return False
