from wsit.main.com.vsi.wsi.wsi_structure import WsiStructure


class TestWsiStructure:
    def test_init(self):
        wsi_structure = WsiStructure()
        assert wsi_structure.alignment() == 0
        assert wsi_structure.length() == 0
        assert wsi_structure.get_value() == wsi_structure

    def test_set_buffer(self):
        wsi_structure = WsiStructure()
        tested_buffer = [1, 2, 3]
        from wsit.main.com.vsi.wsi.wsi_buffer import WsiBuffer
        wsi_buffer = WsiBuffer.init_by_buffer(tested_buffer)
        wsi_structure.set_buffer(wsi_buffer, 0)
        struct_buffer = wsi_structure.buffer()
        for i in range(len(tested_buffer)):
            assert tested_buffer[i] == struct_buffer[i]

    def test_import_structure(self):
        wsi_structure = WsiStructure()
        buffer = [1, 2, 3]
        from wsit.main.com.vsi.wsi.wsi_buffer import WsiBuffer
        wsi_buffer = WsiBuffer.init_by_buffer(buffer)
        wsi_structure.set_buffer(wsi_buffer, 0)
        other_wsi_structure = wsi_structure.import_structure(wsi_buffer)
        assert wsi_structure.__eq__(other_wsi_structure)

    def test_export_structure(self):
        wsi_structure = WsiStructure()
        buffer = [1, 2, 3]
        from wsit.main.com.vsi.wsi.wsi_buffer import WsiBuffer
        wsi_buffer = WsiBuffer.init_by_buffer(buffer)
        wsi_structure.set_buffer(wsi_buffer, 0)
        other_wsi_buffer = WsiBuffer()
        wsi_structure.export_structure(other_wsi_buffer)
        wsi_buffer_array = wsi_buffer.get_buffer()
        other_wsi_buffer_array = other_wsi_buffer.get_buffer()
        for i in range(len(wsi_buffer_array)):
            assert wsi_buffer_array[i] == other_wsi_buffer_array[i]
