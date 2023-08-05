import pytest
import numpy as np
from wsit.main.pyx.xml.rpc.holders.float_holder_editor import FloatHolderEditor
from wsit.main.pyx.xml.rpc.holders.float_holder import FloatHolder
from wsit.test.pyx.xml.rpc.holders.float_holder_test import TestFloatHolder


class TestFloatHolderEditor:

    def test_init(self):
        float_holder_editor = FloatHolderEditor()
        float_holder = float_holder_editor.get_value()
        assert np.allclose(float_holder.get(), 0.0)

    def test_private_field(self):
        float_holder_editor = FloatHolderEditor()
        with pytest.raises(AttributeError):
            float_holder_editor.value = 123

    def test_set_value(self):
        float_holder_editor = FloatHolderEditor()
        for tested_value in TestFloatHolder.valid_values:
            float_holder = FloatHolder(tested_value)
            float_holder_editor.set_value(float_holder)
            assert np.allclose(tested_value, float_holder_editor.get_value().get())

    def test_set_value_exception(self):
        float_holder_editor = FloatHolderEditor()
        # value must be a FloatHolder only
        for tested_value in TestFloatHolder.valid_values + TestFloatHolder.exception_values:
            with pytest.raises(Exception):
                float_holder_editor.set_value(tested_value)

    def test_set_as_text(self):
        float_holder_editor = FloatHolderEditor()
        for tested_value in TestFloatHolder.valid_values:
            float_holder_editor.set_as_text(str(tested_value))
            assert str(np.float32(tested_value)).__eq__(float_holder_editor.get_as_text())

    def test_set_as_text_exception(self):
        float_holder_editor = FloatHolderEditor()
        # type must be a string representation of a float, valid_values content non string values
        for tested_value in TestFloatHolder.exception_text_values + TestFloatHolder.valid_values:
            with pytest.raises(Exception):
                float_holder_editor.set_as_text(tested_value)
