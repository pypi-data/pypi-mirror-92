from wsit.main.com.vsi.wsi.wsi_utils import WsiUtils


class WsiXADesc:
    XA_RBBASE = 100
    XA_RBROLLBACK = 100
    XA_RBCOMMFAIL = 101
    XA_RBDEADLOCK = 102
    XA_RBINTEGRITY = 103
    XA_RBOTHER = 104
    XA_RBPROTO = 105
    XA_RBTIMEOUT = 106
    XA_RBTRANSIENT = 107
    XA_RBEND = 107
    XA_NOMIGRATE = 9
    XA_HEURHAZ = 8
    XA_HEURCOM = 7
    XA_HEURRB = 6
    XA_HEURMIX = 5
    XA_RETRY = 4
    XA_RDONLY = 3
    XAER_ASYNC = -2
    XAER_RMERR = -3
    XAER_NOTA = -4
    XAER_INVAL = -5
    XAER_PROTO = -6
    XAER_RMFAIL = -7
    XAER_DUPID = -8
    XAER_OUTSIDE = -9

    # Convert the error code into a descriptive string.  The format of the
    #  error string is:
    #  <p>
    #  (errcode) xa-standard-description
    #
    #  @param  xaErr       XA error code
    #  @return descriptive string
    @staticmethod
    def err_to_string(xa_err: int) -> str:
        WsiUtils.check_type(xa_err, int)
        err_to_str_dict = {
            WsiXADesc.XA_HEURCOM: "The transaction branch has been heuristically committed.",
            WsiXADesc.XA_HEURHAZ: "The transaction branch may have been heuristically completed.",
            WsiXADesc.XA_HEURMIX: "The transaction branch has been heuristically committed and rolled back.",
            WsiXADesc.XA_HEURRB: "The transaction branch has been heuristically rolled back.",
            WsiXADesc.XA_NOMIGRATE: "Resumption must occur where suspension occured.",
            WsiXADesc.XA_RBCOMMFAIL: "Rollback was caused by communication failure.",
            WsiXADesc.XA_RBDEADLOCK: "A deadlock was detected.",
            WsiXADesc.XA_RBINTEGRITY: "A condition that violates the integrity of the resource was detected.",
            WsiXADesc.XA_RBOTHER: "The resource manager rolled back the transaction branch for a reason not on this list.",
            WsiXADesc.XA_RBPROTO: "A protocol error occured in the resource manager.",
            WsiXADesc.XA_RBROLLBACK: "Rollback was caused by unspecified reason.",
            WsiXADesc.XA_RBTIMEOUT: "A transaction branch took too long.",
            WsiXADesc.XA_RBTRANSIENT: "May retry the transaction branch.",
            WsiXADesc.XA_RDONLY: "The transaction branch has been read-only and has been committed.",
            WsiXADesc.XA_RETRY: "Routine returned with no effect and may be reissued.",
            WsiXADesc.XAER_ASYNC: "Asynchronous operation already outstanding.",
            WsiXADesc.XAER_DUPID: "The XID already exists.",
            WsiXADesc.XAER_INVAL: "Invalid arguments were given.",
            WsiXADesc.XAER_NOTA: "The XID is not valid.",
            WsiXADesc.XAER_OUTSIDE: "The resource manager is doing work outside global transaction.",
            WsiXADesc.XAER_PROTO: "Routine was invoked in an inproper context.",
            WsiXADesc.XAER_RMERR: "A resource manager error has occured in the transaction branch.",
            WsiXADesc.XAER_RMFAIL: "Resource manager is unavailable."
        }
        s = err_to_str_dict.get(xa_err, "Unknown or illegal XA error code")
        return "(" + str(xa_err) + ") " + s

    #  Convert the error code into a descriptive string, and attach the
    #  message from the supplied exception.  The format of the error
    #  string is:
    #  <p>
    #  (errcode) xa-standard-description : exception string
    #
    #  @param  xaErr       XA error code
    #  @param  e           exception string
    #  @return descriptive string
    @staticmethod
    def err_to_string_e(xa_err: int, e: Exception) -> str:
        WsiUtils.check_type(xa_err, int)
        WsiUtils.check_instance(e, Exception)
        return WsiXADesc.err_to_string(xa_err) + ": " + e.args[0]

    def __setattr__(self, name, value):
        WsiUtils.check_set_attr(self, name, value)
