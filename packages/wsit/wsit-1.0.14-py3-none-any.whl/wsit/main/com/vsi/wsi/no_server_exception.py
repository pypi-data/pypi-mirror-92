from wsit.main.com.vsi.wsi.wsi_exception import WsiException


class NoServerException(WsiException):
    def __init__(self):
        super().__init__()

    @classmethod
    def init_from_er_msg(cls, er_message: str) -> 'NoServerException':
        return super().init_from_er_msg(er_message)
