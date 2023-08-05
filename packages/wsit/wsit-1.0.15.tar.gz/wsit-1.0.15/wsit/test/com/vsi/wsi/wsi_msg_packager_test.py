from wsit.main.com.vsi.wsi.wsi_msg_packager import WsiMsgPackager


class TestWsiRtlVersion:
    def test_init(self):
        wsiMsgPackager = WsiMsgPackager()

        DSCsK_DTYPE_Z_Test = 0    # unspecified
        assert wsiMsgPackager.DSCsK_DTYPE_Z == DSCsK_DTYPE_Z_Test

        DSCsK_DTYPE_BU_Test = 2   # byte(unsigned); 8 - bit unsigned quantity
        assert wsiMsgPackager.DSCsK_DTYPE_BU == DSCsK_DTYPE_BU_Test

        DSCsK_DTYPE_WU_Test = 3   # word(unsigned); 16 - bit unsigned quantity
        assert wsiMsgPackager.DSCsK_DTYPE_WU == DSCsK_DTYPE_WU_Test

        DSCsK_DTYPE_LU_Test = 4   # longword(unsigned); 32 - bit unsigned quantity
        assert wsiMsgPackager.DSCsK_DTYPE_LU == DSCsK_DTYPE_LU_Test

        DSCsK_DTYPE_QU_Test = 5   # quadword(unsigned); 64 - bit unsigned quantity
        assert wsiMsgPackager.DSCsK_DTYPE_QU == DSCsK_DTYPE_QU_Test

        DSCsK_DTYPE_OU_Test = 25  # octaword(unsigned); 128 - bit unsigned quantity
        assert wsiMsgPackager.DSCsK_DTYPE_OU == DSCsK_DTYPE_OU_Test

        DSCsK_DTYPE_B_Test = 6    # byte integer(signed); 8 - bit signed 2 's-complement integer
        assert wsiMsgPackager.DSCsK_DTYPE_B == DSCsK_DTYPE_B_Test

        DSCsK_DTYPE_W_Test = 7    # word integer(signed); 16 - bit signed 2 's-complement integer
        assert wsiMsgPackager.DSCsK_DTYPE_W == DSCsK_DTYPE_W_Test

        DSCsK_DTYPE_L_Test = 8    # longword integer(signed); 32 - bit signed 2 's-complement integer
        assert wsiMsgPackager.DSCsK_DTYPE_L == DSCsK_DTYPE_L_Test

        DSCsK_DTYPE_Q_Test = 9    # quadword integer(signed); 64 - bit signed 2 's-complement integer
        assert wsiMsgPackager.DSCsK_DTYPE_Q == DSCsK_DTYPE_Q_Test

        DSCsK_DTYPE_O_Test = 26   # octaword integer(signed); 128 - bit signed 2 's-complement integer
        assert wsiMsgPackager.DSCsK_DTYPE_O == DSCsK_DTYPE_O_Test

        DSCsK_DTYPE_F_Test = 10   # F_floating; 32 - bit single - precision floating point
        assert wsiMsgPackager.DSCsK_DTYPE_F == DSCsK_DTYPE_F_Test

        DSCsK_DTYPE_D_Test = 11   # D_floating; 64 - bit double - precision floating point
        assert wsiMsgPackager.DSCsK_DTYPE_D == DSCsK_DTYPE_D_Test

        DSCsK_DTYPE_G_Test = 27   # G_floating; 64 - bit double - precision floating point
        assert wsiMsgPackager.DSCsK_DTYPE_G == DSCsK_DTYPE_G_Test

        DSCsK_DTYPE_H_Test = 28   # H_floating; 128 - bit quadruple - precision floating point
        assert wsiMsgPackager.DSCsK_DTYPE_H == DSCsK_DTYPE_H_Test

        DSCsK_DTYPE_FC_Test = 12   # F_floating complex
        assert wsiMsgPackager.DSCsK_DTYPE_FC == DSCsK_DTYPE_FC_Test

        DSCsK_DTYPE_DC_Test = 13   # D_floating complex
        assert wsiMsgPackager.DSCsK_DTYPE_DC == DSCsK_DTYPE_DC_Test

        DSCsK_DTYPE_GC_Test = 29   # G_floating complex
        assert wsiMsgPackager.DSCsK_DTYPE_GC == DSCsK_DTYPE_GC_Test

        DSCsK_DTYPE_HC_Test = 30   # H_floating complex
        assert wsiMsgPackager.DSCsK_DTYPE_HC == DSCsK_DTYPE_HC_Test

        DSCsK_DTYPE_CIT_Test = 31
        assert wsiMsgPackager.DSCsK_DTYPE_CIT == DSCsK_DTYPE_CIT_Test

        DSCsK_DTYPE_T_Test = 14    # character string; a single 8 - bit character or a sequence of characters
        assert wsiMsgPackager.DSCsK_DTYPE_T == DSCsK_DTYPE_T_Test

        DSCsK_DTYPE_VT_Test = 37   # varying character string; 16 - bit count, followed by a string
        assert wsiMsgPackager.DSCsK_DTYPE_VT == DSCsK_DTYPE_VT_Test

        DSCsK_DTYPE_NU_Test = 15   # numeric string, unsigned
        assert wsiMsgPackager.DSCsK_DTYPE_NU == DSCsK_DTYPE_NU_Test

        DSCsK_DTYPE_NL_Test = 16   # numeric string, left separate sign
        assert wsiMsgPackager.DSCsK_DTYPE_NL == DSCsK_DTYPE_NL_Test

        DSCsK_DTYPE_NLO_Test = 17  # numeric string, left overpunch0ed sign
        assert wsiMsgPackager.DSCsK_DTYPE_NLO == DSCsK_DTYPE_NLO_Test

        DSCsK_DTYPE_NR_Test = 18   # numeric string, right separate sign
        assert wsiMsgPackager.DSCsK_DTYPE_NR == DSCsK_DTYPE_NR_Test

        DSCsK_DTYPE_NRO_Test = 19  # numeric string, right overpunched sign
        assert wsiMsgPackager.DSCsK_DTYPE_NRO == DSCsK_DTYPE_NRO_Test

        DSCsK_DTYPE_NZ_Test = 20   # numeric string, zoned sign
        assert wsiMsgPackager.DSCsK_DTYPE_NZ == DSCsK_DTYPE_NZ_Test

        DSCsK_DTYPE_P_Test = 21    # packed decimal string
        assert wsiMsgPackager.DSCsK_DTYPE_P == DSCsK_DTYPE_P_Test

        DSCsK_DTYPE_V_Test = 1     # aligned bit string
        assert wsiMsgPackager.DSCsK_DTYPE_V == DSCsK_DTYPE_V_Test

        DSCsK_DTYPE_VU_Test = 34   # unaligned bit string
        assert wsiMsgPackager.DSCsK_DTYPE_VU == DSCsK_DTYPE_VU_Test

        DSCsK_DTYPE_FS_Test = 52   # IEEE float basic single S
        assert wsiMsgPackager.DSCsK_DTYPE_FS == DSCsK_DTYPE_FS_Test

        DSCsK_DTYPE_FT_Test = 53   # IEEE float basic double T
        assert wsiMsgPackager.DSCsK_DTYPE_FT == DSCsK_DTYPE_FT_Test

        DSCsK_DTYPE_FSC_Test = 54  # IEEE float basic single S complex
        assert wsiMsgPackager.DSCsK_DTYPE_FSC == DSCsK_DTYPE_FSC_Test

        DSCsK_DTYPE_FTC_Test = 55  # IEEE float basic double T complex
        assert wsiMsgPackager.DSCsK_DTYPE_FTC == DSCsK_DTYPE_FTC_Test

        DSCsK_DTYPE_FX_Test = 57   # IEEE float basic extended
        assert wsiMsgPackager.DSCsK_DTYPE_FX == DSCsK_DTYPE_FX_Test

        DSCsK_DTYPE_FXC_Test = 58  # IEEE float complex extended
        assert wsiMsgPackager.DSCsK_DTYPE_FXC == DSCsK_DTYPE_FXC_Test

        DSCsK_DTYPE_ZI_Test = 22   # sequence of instructions
        assert wsiMsgPackager.DSCsK_DTYPE_ZI == DSCsK_DTYPE_ZI_Test

        DSCsK_DTYPE_ZEM_Test = 23  # procedure entry mask
        assert wsiMsgPackager.DSCsK_DTYPE_ZEM == DSCsK_DTYPE_ZEM_Test

        DSCsK_DTYPE_DSC_Test = 24  # descriptor
        assert wsiMsgPackager.DSCsK_DTYPE_DSC == DSCsK_DTYPE_DSC_Test

        DSCsK_DTYPE_BPV_Test = 32  # bound procedure value
        assert wsiMsgPackager.DSCsK_DTYPE_BPV == DSCsK_DTYPE_BPV_Test

        DSCsK_DTYPE_BLV_Test = 33  # bound label value
        assert wsiMsgPackager.DSCsK_DTYPE_BLV == DSCsK_DTYPE_BLV_Test

        DSCsK_DTYPE_ADT_Test = 35  # absolute date and time
        assert wsiMsgPackager.DSCsK_DTYPE_ADT == DSCsK_DTYPE_ADT_Test

        DSCsK_DTYPE_STRUCT_Test = 77  # BWX Structure
        assert wsiMsgPackager.DSCsK_DTYPE_STRUCT == DSCsK_DTYPE_STRUCT_Test

        DSCsK_CLASS_S_Test = 1        # Static / Scalar
        assert wsiMsgPackager.DSCsK_CLASS_S == DSCsK_CLASS_S_Test

        DSCsK_CLASS_D_Test = 2        # Dynamic String
        assert wsiMsgPackager.DSCsK_CLASS_D == DSCsK_CLASS_D_Test

        DSCsK_CLASS_A_Test = 4        # Array
        assert wsiMsgPackager.DSCsK_CLASS_A == DSCsK_CLASS_A_Test

        DSCsK_CLASS_SD_Test = 9       # Scaled Decimal
        assert wsiMsgPackager.DSCsK_CLASS_SD == DSCsK_CLASS_SD_Test

        DSCsK_CLASS_NCA_Test = 10     # Non - Contiguous Array
        assert wsiMsgPackager.DSCsK_CLASS_NCA == DSCsK_CLASS_NCA_Test

        DSCsK_CLASS_VS_Test = 11      # Variant String
        assert wsiMsgPackager.DSCsK_CLASS_VS == DSCsK_CLASS_VS_Test

        DSCsK_CLASS_VSA_Test = 12     # Variant String Array
        assert wsiMsgPackager.DSCsK_CLASS_VSA == DSCsK_CLASS_VSA_Test

    def test_init_by_buf_size(self):
        array_size = 5
        bytes = [0, 0, 0, 0, 0]
        wsi_msg_packager = WsiMsgPackager.init_by_buf_size(array_size)
        assert wsi_msg_packager.get_buffer_internal() == bytes
        assert wsi_msg_packager.get_buf_size() == array_size

    def test_init_by_buffer_buf_base(self):
        bytes = [1, 2, 3]
        tested_value = 3
        wsi_msg_packager = WsiMsgPackager.init_by_buffer_buf_base(bytes, tested_value)
        assert wsi_msg_packager.get_buffer_internal() == bytes
        assert wsi_msg_packager.get_buf_size() == len(bytes)
        assert wsi_msg_packager.get_base() == tested_value

        bytes = []
        tested_value = 0
        wsi_msg_packager = WsiMsgPackager.init_by_buffer_buf_base(bytes, tested_value)
        assert wsi_msg_packager.get_buffer_internal() == []
        assert wsi_msg_packager.get_buf_size() == tested_value
        assert wsi_msg_packager.get_base() == tested_value
