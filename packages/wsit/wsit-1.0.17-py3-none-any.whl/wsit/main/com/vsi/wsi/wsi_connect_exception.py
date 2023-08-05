from wsit.main.com.vsi.wsi.wsi_exception import WsiException


class WsiConnectException(WsiException):
    def __init__(self):
        super().__init__()

    @classmethod
    def init_from_er_msg(cls, er_message: str) -> 'WsiConnectException':
        return super().init_from_er_msg(er_message)

    @classmethod
    def init_from_er_msg_ex_code_vms_code(cls, er_message: str, in_exc_code: int,
                                          in_vms_code: int) -> 'WsiConnectException':
        return super().init_from_er_msg_ex_code_vms_code(er_message, in_exc_code, in_vms_code)

    @classmethod
    def init_from_er_msg_ex_code_vms_code_severity_facility(cls, er_message: str, in_exc_code: int, in_vms_code: int,
                                                            in_severity: int,
                                                            in_facility: int) -> 'WsiConnectException':
        return super().init_from_er_msg_ex_code_vms_code_severity_facility(er_message, in_exc_code, in_vms_code,
                                                                           in_severity, in_facility)

    @classmethod
    def init_from_wsi_exception(cls, wsi_ex) -> 'WsiConnectException':
        return super().init_from_wsi_exception(wsi_ex)
