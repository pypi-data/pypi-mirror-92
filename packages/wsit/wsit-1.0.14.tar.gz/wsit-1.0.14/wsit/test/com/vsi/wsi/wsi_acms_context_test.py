import pytest

from wsit.main.com.vsi.wsi.wsi_acms_context import WsiAcmsContext


class TestWsiAcmsContext:
    exception_values = [True, False, 234.890, -7389457908.39485797, 23784629846, -98753948, 0, 1]
    valid_values = ["selection string", 'selection string', "a", 'b', "", "True", "False", "0", '0', "1", '1',
                    '124.9090798', '-0.126155', "-803485.9457897", "4564690846908.4059680458960", "485739857",
                    "-4573875937",  "None", 'None']
    valid_text_values = ["selection string", 'selection string', "a", 'b', "", "True", "False", "0", '0', "1", '1',
                    '124.9090798', '-0.126155', "-803485.9457897", "4564690846908.4059680458960", "485739857",
                    "-4573875937", "None", 'None']
    exception_text_values = ["selection string", 'selection string', "a", 'b', "", "True", "False", "0", '0', "1", '1',
                             '124.9090798', '-0.126155', "-803485.9457897", "4564690846908.4059680458960", "485739857",
                             "-4573875937", "None", 'None', True, False, 234.890, -7389457908.39485797, 23784629846,
                             -98753948, 0, 1]

    def test_init(self):
        wsi_acms_context = WsiAcmsContext()
        assert wsi_acms_context.get_sel_string() is None
        assert wsi_acms_context.get_ext_status() is None
        assert wsi_acms_context.get_app_name() is None

    def test_private_field(self):
        wsi_acms_context = WsiAcmsContext()
        with pytest.raises(AttributeError):
            wsi_acms_context.value = 123

    def test_init_by_sel_str(self):
        for tested_value in TestWsiAcmsContext.valid_values:
            wsi_acms_context = WsiAcmsContext.init_by_sel_str(tested_value)
            assert wsi_acms_context.get_sel_string() == tested_value

    def test_init_exception(self):
        for tested_value in TestWsiAcmsContext.exception_values:
            with pytest.raises(Exception):
                wsi_acms_context = WsiAcmsContext(tested_value)

    def test_set_sel_string(self):
        for tested_value in TestWsiAcmsContext.valid_values:
            wsi_acms_context = WsiAcmsContext()
            wsi_acms_context.set_sel_string(tested_value)
            assert wsi_acms_context.get_sel_string().__eq__(tested_value)

    def test_set_ext_status(self):
        for tested_value in TestWsiAcmsContext.valid_values:
            wsi_acms_context = WsiAcmsContext()
            wsi_acms_context.set_ext_status(tested_value)
            assert wsi_acms_context.get_ext_status().__eq__(tested_value)

    def test_set_app_name(self):
        for tested_value in TestWsiAcmsContext.valid_values:
            wsi_acms_context = WsiAcmsContext()
            wsi_acms_context.set_app_name(tested_value)
            assert wsi_acms_context.get_app_name().__eq__(tested_value)

    def test_to_string(self):
        for tested_value in TestWsiAcmsContext.valid_text_values:
            wsi_acms_context = WsiAcmsContext()
            tested_value_to_string = "Selection String = " + tested_value + "\n" + "Extended Status = " + tested_value \
                                     + "\n" + "Application Name = " + tested_value
            wsi_acms_context.set_sel_string(tested_value)
            wsi_acms_context.set_ext_status(tested_value)
            wsi_acms_context.set_app_name(tested_value)
            assert wsi_acms_context.__str__().__eq__(tested_value_to_string)
