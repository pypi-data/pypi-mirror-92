from wsit.main.com.vsi.wsi.i_wsi_native_shell import IWsiNativeShell
from wsit.main.com.vsi.wsi.i_xid import IXid
from wsit.main.com.vsi.wsi.wsi_xid_map import WsiXIDMap


class TestWsiXIDMap:
    __wsi_xid_map = WsiXIDMap.get_xid_map()
    __empty_value = "com.hp.wsi.WsiXIDMap contents:\n\t-- empty --\n"
    __xid = IXid()
    __wsi_native_shell = IWsiNativeShell()
    __other_wsi_native_shell = IWsiNativeShell()

    def test_init(self):
        assert self.__wsi_xid_map.__str__().__eq__(self.__empty_value)
        assert self.__wsi_xid_map.get_xid_map().__eq__(self.__wsi_xid_map)

    def test_add_if_remove(self):
        self.__wsi_xid_map.add_if(self.__xid, self.__wsi_native_shell)
        tested_b_value_one = "com.hp.wsi.WsiXIDMap contents:\n"
        tested_b_value_one += "    xid = " + str(self.__xid) + "\n\t"
        tested_b_value_one += "values = {\n        " + str(self.__wsi_native_shell) + "\n    }\n"
        assert tested_b_value_one.__eq__(self.__wsi_xid_map.__str__())

        self.__wsi_xid_map.add_if(self.__xid, self.__other_wsi_native_shell)
        tested_b_value_two = "com.hp.wsi.WsiXIDMap contents:\n"
        tested_b_value_two += "    xid = " + str(self.__xid) + "\n\t"
        tested_b_value_two += "values = {\n        " + str(self.__wsi_native_shell) + "\n"
        tested_b_value_two += "        " + str(self.__other_wsi_native_shell) + "\n"
        tested_b_value_two += "    }\n"
        assert tested_b_value_two.__eq__(self.__wsi_xid_map.__str__())

        self.__wsi_xid_map.remove(self.__xid, self.__other_wsi_native_shell)
        assert tested_b_value_one.__eq__(self.__wsi_xid_map.__str__())
        self.__wsi_xid_map.remove(self.__xid, self.__wsi_native_shell)
        assert self.__empty_value.__eq__(self.__wsi_xid_map.__str__())
