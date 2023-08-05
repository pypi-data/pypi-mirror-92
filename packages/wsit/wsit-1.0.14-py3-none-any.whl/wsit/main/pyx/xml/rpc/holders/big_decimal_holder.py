from wsit.main.com.vsi.wsi.big_decimal import BigDecimal
from wsit.main.pyx.xml.rpc.holders.holder import Holder


class BigDecimalHolder(Holder):

    def __init__(self, new_value=BigDecimal.init_from_str("0.0")):
        self.set(new_value)

    def set(self, new_value):
        if type(new_value) is BigDecimal:
            super().set(new_value)
        else:
            raise ValueError("value must be a decimal type")

    def __eq__(self, obj):
        if isinstance(obj, BigDecimalHolder):
            return self.get() == obj.get()
        return False
