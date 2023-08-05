from wsit.main.com.vsi.wsi.big_decimal import BigDecimal
from wsit.main.pyx.xml.rpc.holders.holder_editor import HolderEditor


class BigDecimalEditor(HolderEditor):

    def __init__(self):
        super().__init__(BigDecimal.init_from_str("0.0"))

    def set_value(self, new_value):
        if type(new_value) is BigDecimal:
            super().set_value(new_value)
        else:
            raise ValueError("value must be a decimal type")

    def set_as_text(self, new_value):
        try:
            if type(new_value) is str:
                super().set_value(BigDecimal.init_from_str(new_value))
            else:
                raise TypeError("value must be a string representation of a decimal")
        except Exception as ex:
            raise ValueError(ex.args[0])
