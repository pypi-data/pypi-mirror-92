
from wsit.main.com.vsi.wsi.big_decimal import BigDecimal
from wsit.main.pyx.xml.rpc.holders.big_decimal_holder import BigDecimalHolder
from wsit.main.pyx.xml.rpc.holders.holder_editor import HolderEditor


class BigDecimalHolderEditor(HolderEditor):

    def __init__(self):
        super().__init__(BigDecimalHolder())

    def set_value(self, new_value):
        if isinstance(new_value, BigDecimalHolder):
            super().set_value(new_value)
        else:
            raise ValueError("value must be a BigDecimalHolder type")

    def set_as_text(self, new_value):
        try:
            if type(new_value) is str:
                super().get_value().set(BigDecimal.init_from_str(new_value))
            else:
                raise ValueError("value must be a string representation of a decimal")
        except Exception as ex:
            raise ValueError(ex.args[0])
