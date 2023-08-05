import numpy as np
import pytest
from wsit.main.pyx.xml.rpc.holders.double_holder import DoubleHolder


class TestDoubleHolder:

    exception_values = ["value", 'string', 'a', "b", '', "", True, False, "True", "False", "0", "1", '0', '1',
                        '124.9090798', '-0.126155', "-803485.9457897", "4564690846908.4059680458960", "485739857",
                        "-4573875937", None, "None", 'None']

    exception_text_values = ["value", 'string', 'a', "b", '', "", True, False, "True", "False", None, "None", 'None']

    valid_values = [9007199254740994000, 1.7e-308, 1.7e308, 0.0, 1.4e-450, 3.4028235e38,
                    16777216, -16777216, 0, 1, -389475, -1.4e-450, -3.4028235e38, -0, -1]

    def test_init(self):
        double_holder = DoubleHolder()
        assert np.allclose(double_holder.get(), 0.0)

    def test_init_param(self):
        for tested_value in TestDoubleHolder.valid_values:
            double_holder = DoubleHolder(tested_value)
            assert np.allclose(double_holder.get(), tested_value)

    def test_init_param_exception(self):
        for tested_value in TestDoubleHolder.exception_values:
            with pytest.raises(Exception):
                double_holder = DoubleHolder(tested_value)

    def test_private_field(self):
        double_holder = DoubleHolder()
        with pytest.raises(AttributeError):
            double_holder.value = 123

    def test_to_string(self):
        for tested_value in TestDoubleHolder.valid_values:
            double_holder = DoubleHolder(tested_value)
            assert double_holder.__str__().__eq__(float(tested_value).__str__())

    def test_equals(self):
        double_holder_1 = DoubleHolder()
        double_holder_2 = DoubleHolder()
        assert double_holder_1.__eq__(None) is False
        assert double_holder_1.__eq__(int("123")) is False
        assert double_holder_1.__eq__(double_holder_1) is True
        assert double_holder_1.__eq__(double_holder_2) is True
        double_holder_2.set(1234561213456.12)
        assert double_holder_1.__eq__(double_holder_2) is False
