from typing import List

from wsit.main.com.vsi.wsi.i_xa_resource import IXAResource
from wsit.main.com.vsi.wsi.server_config import ServerConfig
from wsit.main.com.vsi.wsi.wsi_utils import WsiUtils
from wsit.main.pyx.xml.rpc.holders.byte_holder import ByteHolder


class IWsiNativeShell:
    def init(self, cfg: ServerConfig):
        WsiUtils.check_instance(cfg, ServerConfig)

    def destroy(self):
        pass

    def get_xa_resource(self) -> IXAResource:
        return None

    def supports_local_tx(self) -> bool:
        return False

    def supports_global_tx(self) -> bool:
        return False

    def get_eis_mame(self) -> str:
        return None

    def get_eis_version(self) -> str:
        return None

    def get_file(self, file_id: int) -> List[ByteHolder]:
        WsiUtils.check_type(file_id, int)
        sbyte_list = List[ByteHolder]
        return sbyte_list

    def invoke_dcl(self, dcl_id: int, command: str, termout: bool) -> List[ByteHolder]:
        WsiUtils.check_type(dcl_id, int)
        WsiUtils.check_type(command, str)
        WsiUtils.check_type(termout, bool)
        sbyte_list = List[ByteHolder]
        return sbyte_list

    def invoke(self, method_id: int, in_buf: List[ByteHolder], buf_used_len: int) -> List[ByteHolder]:
        WsiUtils.check_type(method_id, int)
        WsiUtils.check_type(in_buf, List[ByteHolder])
        WsiUtils.check_type(buf_used_len, int)
        sbyte_list = List[ByteHolder]
        return sbyte_list

    def acms_sign_in(self, user_name: str):
        WsiUtils.check_type(user_name, str)
        pass

    def acms_sign_out(self):
        pass

    def vms_login(self, user_name: str, password: str):
        WsiUtils.check_type(user_name, str)
        WsiUtils.check_type(password, str)

    def vms_logout(self):
        pass

    def load_domain(self):
        pass

    def set_ipc_state(self, lock_flag: int):
        WsiUtils.check_type(lock_flag, int)

    def is_bad_shell(self) -> bool:
        return False

    def set_bad_shell(self):
        pass
