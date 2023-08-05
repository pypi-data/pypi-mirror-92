class XAException(Exception):
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

    def __init__(self, arg):
        if type(arg) is int:
            self.error_code = arg
        elif type(arg) is str:
            super.__init__(arg)
        else:
            raise TypeError("Wrong type for argument: " + str(type(arg)))
