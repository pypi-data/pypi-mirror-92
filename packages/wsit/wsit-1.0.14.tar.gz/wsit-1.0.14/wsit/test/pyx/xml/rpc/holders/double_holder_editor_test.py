import pytest
import numpy as np
from wsit.main.pyx.xml.rpc.holders.double_holder_editor import DoubleHolderEditor
from wsit.main.pyx.xml.rpc.holders.double_holder import DoubleHolder
from wsit.test.pyx.xml.rpc.holders.double_holder_test import TestDoubleHolder


class TestDoubleHolderEditor:

    def test_init(self):
        double_holder_editor = DoubleHolderEditor()
        double_holder = double_holder_editor.get_value()
        assert np.allclose(double_holder.get(), 0.0)

    def test_private_field(self):
        double_holder_editor = DoubleHolderEditor()
        with pytest.raises(AttributeError):
            double_holder_editor.value = 123

    def test_set_value(self):
        double_holder_editor = DoubleHolderEditor()
        for tested_value in TestDoubleHolder.valid_values:
            double_holder = DoubleHolder(tested_value)
            double_holder_editor.set_value(double_holder)
            assert np.allclose(tested_value, double_holder_editor.get_value().get())

    def test_set_value_exception(self):
        double_holder_editor = DoubleHolderEditor()
        # value must be a DoubleHolder only
        for tested_value in TestDoubleHolder.valid_values + TestDoubleHolder.exception_values:
            with pytest.raises(Exception):
                double_holder_editor.set_value(tested_value)

    def test_set_as_text(self):
        double_holder_editor = DoubleHolderEditor()
        for tested_value in TestDoubleHolder.valid_values:
            double_holder_editor.set_as_text(str(tested_value))
            assert str(float(tested_value)).__eq__(double_holder_editor.get_as_text())

    def test_set_as_text_exception(self):
        double_holder_editor = DoubleHolderEditor()
        # type must be a string representation of a double, valid_values content non string values
        for tested_value in TestDoubleHolder.exception_text_values + TestDoubleHolder.valid_values:
            with pytest.raises(Exception):
                double_holder_editor.set_as_text(tested_value)
