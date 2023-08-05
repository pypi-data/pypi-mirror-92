import pytest

from wsit.main.com.vsi.wsi.wsi_xa_desc import WsiXADesc


class TestWsiXADesc:
    valid_values = {
        WsiXADesc.XA_HEURCOM:
            "(" + str(WsiXADesc.XA_HEURCOM) + ") The transaction branch has been heuristically committed.",
        WsiXADesc.XA_HEURHAZ:
            "(" + str(WsiXADesc.XA_HEURHAZ) + ") The transaction branch may have been heuristically completed.",
        WsiXADesc.XA_HEURMIX:
            "(" + str(WsiXADesc.XA_HEURMIX) + ") The transaction branch has been heuristically committed and rolled back.",
        WsiXADesc.XA_HEURRB:
            "(" + str(WsiXADesc.XA_HEURRB) + ") The transaction branch has been heuristically rolled back.",
        WsiXADesc.XA_NOMIGRATE:
            "(" + str(WsiXADesc.XA_NOMIGRATE) + ") Resumption must occur where suspension occured.",
        WsiXADesc.XA_RBCOMMFAIL:
            "(" + str(WsiXADesc.XA_RBCOMMFAIL) + ") Rollback was caused by communication failure.",
        WsiXADesc.XA_RBDEADLOCK:
            "(" + str(WsiXADesc.XA_RBDEADLOCK) + ") A deadlock was detected.",
        WsiXADesc.XA_RBINTEGRITY:
            "(" + str(WsiXADesc.XA_RBINTEGRITY) + ") A condition that violates the integrity of the resource was detected.",
        WsiXADesc.XA_RBOTHER:
            "(" + str(WsiXADesc.XA_RBOTHER) + ") The resource manager rolled back the transaction branch for a reason not on this list.",
        WsiXADesc.XA_RBPROTO:
            "(" + str(WsiXADesc.XA_RBPROTO) + ") A protocol error occured in the resource manager.",
        WsiXADesc.XA_RBROLLBACK:
            "(" + str(WsiXADesc.XA_RBROLLBACK) + ") Rollback was caused by unspecified reason.",
        WsiXADesc.XA_RBTIMEOUT:
            "(" + str(WsiXADesc.XA_RBTIMEOUT) + ") A transaction branch took too long.",
        WsiXADesc.XA_RBTRANSIENT:
            "(" + str(WsiXADesc.XA_RBTRANSIENT) + ") May retry the transaction branch.",
        WsiXADesc.XA_RDONLY:
            "(" + str(WsiXADesc.XA_RDONLY) + ") The transaction branch has been read-only and has been committed.",
        WsiXADesc.XA_RETRY:
            "(" + str(WsiXADesc.XA_RETRY) + ") Routine returned with no effect and may be reissued.",
        WsiXADesc.XAER_ASYNC:
            "(" + str(WsiXADesc.XAER_ASYNC) + ") Asynchronous operation already outstanding.",
        WsiXADesc.XAER_DUPID:
            "(" + str(WsiXADesc.XAER_DUPID) + ") The XID already exists.",
        WsiXADesc.XAER_INVAL:
            "(" + str(WsiXADesc.XAER_INVAL) + ") Invalid arguments were given.",
        WsiXADesc.XAER_NOTA:
            "(" + str(WsiXADesc.XAER_NOTA) + ") The XID is not valid.",
        WsiXADesc.XAER_OUTSIDE:
            "(" + str(WsiXADesc.XAER_OUTSIDE) + ") The resource manager is doing work outside global transaction.",
        WsiXADesc.XAER_PROTO:
            "(" + str(WsiXADesc.XAER_PROTO) + ") Routine was invoked in an inproper context.",
        WsiXADesc.XAER_RMERR:
            "(" + str(WsiXADesc.XAER_RMERR) + ") A resource manager error has occured in the transaction branch.",
        WsiXADesc.XAER_RMFAIL:
            "(" + str(WsiXADesc.XAER_RMFAIL) + ") Resource manager is unavailable.",
        777: "(777) Unknown or illegal XA error code",
    }

    def test_err_to_string(self):
        for key in TestWsiXADesc.valid_values.keys():
            assert WsiXADesc.err_to_string(key).__eq__(TestWsiXADesc.valid_values.get(key))

    def test_err_to_string_e(self):
        err = TypeError("Type conversion error")
        for key in TestWsiXADesc.valid_values.keys():
            tested_str = TestWsiXADesc.valid_values.get(key) + ": " + err.args[0]
            assert WsiXADesc.err_to_string_e(key, err).__eq__(tested_str)

    def test_private_field(self):
        wsi_xa_desc = WsiXADesc()
        with pytest.raises(AttributeError):
            wsi_xa_desc.value = 123
