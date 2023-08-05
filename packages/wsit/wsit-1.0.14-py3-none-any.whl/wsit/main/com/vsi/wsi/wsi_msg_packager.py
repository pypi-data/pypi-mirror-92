from typing import List
from wsit.main.com.vsi.wsi.wsi_buffer import WsiBuffer


class WsiMsgPackager(WsiBuffer):
    """
    The following constants are used to identify specific OpenVMS datatypes.
    Atomic data types:
    """
    DSCsK_DTYPE_Z = 0     # unspecified
    DSCsK_DTYPE_BU = 2    # byte (unsigned);  8-bit unsigned quantity
    DSCsK_DTYPE_WU = 3    # word (unsigned);  16-bit unsigned quantity
    DSCsK_DTYPE_LU = 4    # longword (unsigned);  32-bit unsigned quantity
    DSCsK_DTYPE_QU = 5    # quadword (unsigned);  64-bit unsigned quantity
    DSCsK_DTYPE_OU = 25   # octaword (unsigned);  128-bit unsigned quantity
    DSCsK_DTYPE_B = 6     # byte integer (signed);  8-bit signed 2's-complement integer
    DSCsK_DTYPE_W = 7     # word integer (signed);  16-bit signed 2's-complement integer
    DSCsK_DTYPE_L = 8     # longword integer (signed);  32-bit signed 2's-complement integer
    DSCsK_DTYPE_Q = 9     # quadword integer (signed);  64-bit signed 2's-complement integer
    DSCsK_DTYPE_O = 26    # octaword integer (signed);  128-bit signed 2's-complement integer
    DSCsK_DTYPE_F = 10    # F_floating;  32-bit single-precision floating point
    DSCsK_DTYPE_D = 11    # D_floating;  64-bit double-precision floating point
    DSCsK_DTYPE_G = 27    # G_floating;  64-bit double-precision floating point
    DSCsK_DTYPE_H = 28    # H_floating;  128-bit quadruple-precision floating point
    DSCsK_DTYPE_FC = 12   # F_floating complex
    DSCsK_DTYPE_DC = 13   # D_floating complex
    DSCsK_DTYPE_GC = 29   # G_floating complex
    DSCsK_DTYPE_HC = 30   # H_floating complex
    DSCsK_DTYPE_CIT = 31  # COBOL Intermediate Temporary

    # String data types:
    DSCsK_DTYPE_T = 14    # character string;  a single 8-bit character or a sequence of characters
    DSCsK_DTYPE_VT = 37   # varying character string;  16-bit count, followed by a string
    DSCsK_DTYPE_NU = 15   # numeric string, unsigned
    DSCsK_DTYPE_NL = 16   # numeric string, left separate sign
    DSCsK_DTYPE_NLO = 17  # numeric string, left overpunched sign
    DSCsK_DTYPE_NR = 18   # numeric string, right separate sign
    DSCsK_DTYPE_NRO = 19  # numeric string, right overpunched sign
    DSCsK_DTYPE_NZ = 20   # numeric string, zoned sign
    DSCsK_DTYPE_P = 21    # packed decimal string
    DSCsK_DTYPE_V = 1     # aligned bit string
    DSCsK_DTYPE_VU = 34   # unaligned bit string

    # IEEE data types:
    DSCsK_DTYPE_FS = 52   # IEEE float basic single S
    DSCsK_DTYPE_FT = 53   # IEEE float basic double T
    DSCsK_DTYPE_FSC = 54  # IEEE float basic single S complex
    DSCsK_DTYPE_FTC = 55  # IEEE float basic double T complex
    DSCsK_DTYPE_FX = 57   # IEEE float basic extended
    DSCsK_DTYPE_FXC = 58  # IEEE float complex extended

    # Miscellaneous data types:
    DSCsK_DTYPE_ZI = 22   # sequence of instructions
    DSCsK_DTYPE_ZEM = 23  # procedure entry mask
    DSCsK_DTYPE_DSC = 24  # descriptor
    DSCsK_DTYPE_BPV = 32  # bound procedure value
    DSCsK_DTYPE_BLV = 33  # bound label value
    DSCsK_DTYPE_ADT = 35  # absolute date and time

    # WSIT specific data types:
    DSCsK_DTYPE_STRUCT = 77  # BWX Structure

    # Constants for the various class types encountered
    DSCsK_CLASS_S = 1      # Static/Scalar
    DSCsK_CLASS_D = 2      # Dynamic String
    DSCsK_CLASS_A = 4      # Array
    DSCsK_CLASS_SD = 9     # Scaled Decimal
    DSCsK_CLASS_NCA = 10   # Non-Contiguous Array
    DSCsK_CLASS_VS = 11    # Variant String
    DSCsK_CLASS_VSA = 12   # Variant String Array

    def __init__(self):
        super().__init__()

    @staticmethod
    def init_from_msg_size(msg_size: int):
        return super().init_by_buf_size(msg_size)

    @staticmethod
    def init_from_buffer(buffer: List[int]):
        return super().init_by_buffer(buffer)

    @staticmethod
    def init_from_buffer_msg_base(buffer: List[int], msg_base: int):
        return super().init_by_buffer_buf_base(buffer, msg_base)
