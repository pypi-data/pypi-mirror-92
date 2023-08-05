import pytest

from wsit.main.com.vsi.wsi.string_qualify import StringQualify


class TestStringQualify:
    list_values = ["Beauty\n will\tsafe the \r world",
                   "Hello world",
                   "\'Hello world\'",
                   "\"Hello world\"",
                   "\"Hello\" \"world\"",
                   "   \f   \'the      \"most    difficult\n\"     test\t     ever\'\r      "]

    expected_values = [" \"Beauty will safe the world\"",
                       " \"Hello world\"",
                       " \"''Hello' world'\"",
                       " \"\"\"Hello world\"\"\"",
                       " \"\"\"Hello\"\" \"\"world\"\"\"",
                       " \"''the' \"\"most difficult \"\" test ever'\""]

    def test_format_param(self):
        string_qualify = StringQualify()
        for i in range(len(self.list_values)):
            assert string_qualify.format_param(self.list_values[i]) == self.expected_values[i]
