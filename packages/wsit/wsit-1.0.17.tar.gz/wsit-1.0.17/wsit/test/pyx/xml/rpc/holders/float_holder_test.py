import pytest
import numpy as np

from wsit.main.pyx.xml.rpc.holders.float_holder import FloatHolder


class TestFloatHolder:

    exception_values = ["value", 'string', 'a', "b", '', "", True, False, "True", "False", "0", "1", '0', '1',
                        '124.9090798', '-0.126155', "-803485.9457897", "4564690846908.4059680458960", "485739857",
                        "-4573875937", None, "None", 'None']

    exception_text_values = ["value", 'string', 'a', "b", '', "", True, False, "True", "False", None, "None", 'None']

    valid_values = [np.finfo(np.float32).max, np.finfo(np.float32).min, 0.0, np.float32(1.4e-45), np.float32(3.4028235e38),
                    16777216, -16777216, 0, 1, -389475, np.float32(-1.4e-45), np.float32(-3.4028235e38), -0, -1]

    def test_init(self):
        float_holder = FloatHolder()
        assert np.allclose(float_holder.get(), 0.0)

    def test_private_field(self):
        float_holder = FloatHolder()
        with pytest.raises(AttributeError):
            float_holder.value = 123

    def test_init_param(self):
        for tested_value in TestFloatHolder.valid_values:
            float_holder = FloatHolder(tested_value)
            assert np.allclose(float_holder.get(), tested_value)

    def test_init_param_exception(self):
        for tested_value in TestFloatHolder.exception_values:
            with pytest.raises(Exception):
                float_holder = FloatHolder(tested_value)

    def test_to_string(self):
        for tested_value in TestFloatHolder.valid_values:
            float_holder = FloatHolder(tested_value)
            assert float_holder.__str__().__eq__(np.float32(tested_value).__str__())

    def test_equals(self):
        float_holder_1 = FloatHolder()
        float_holder_2 = FloatHolder()
        assert float_holder_1.__eq__(None) is False
        assert float_holder_1.__eq__(int("123")) is False
        assert float_holder_1.__eq__(float_holder_1) is True
        assert float_holder_1.__eq__(float_holder_2) is True
        float_holder_2.set(123456.12)
        assert float_holder_1.__eq__(float_holder_2) is False
