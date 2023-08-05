from typing import List


class WsiStructure:
    struct_size = 0
    struct_alignment = 0
    struct_buffer = None
    struct_base = 0

    '''
    Return the computed alignment value for this structure.
     @return int alignment value -- a power of two from 1 from 16.
    '''
    def alignment(self) -> int:
        return self.struct_alignment


    '''
    Return the size for this structure.
    @return int size value
    '''
    def length(self) -> int:
        return self.struct_size

    '''Return & Set this structure.'''
    def get_value(self) -> 'WsiStructure':
        return self

    '''Sets the underlining buffer for this structure'''
    def set_buffer(self, parent_buffer: 'WsiBuffer', buf_base: int):
        from wsit.main.com.vsi.wsi.wsi_buffer import WsiBuffer
        self.struct_buffer = WsiBuffer.init_by_wsi_buffer_buf_base(parent_buffer, buf_base)

    '''public abstract void setValue (WsiStructure inbuffer) throws Exception;'''
    def set_value(self, in_buffer: 'WsiStructure'):
        pass

    '''public abstract WsiBuffer wsiBuffer() throws Exception;'''
    def wsi_buffer(self):
        return self.struct_buffer

    def buffer(self) -> List[int]:
        return self.struct_buffer.get_buffer()

    '''public abstract void Buffer (byte [] newbuffer) throws Exception;'''

    '''public abstract void Buffer (byte [] newbuffer, int offset) throws Exception;'''
    def buffer_from_buffer_offset(self, new_buffer: List[int], offset: int):
        pass

    '''These routines are used internally by the data marshalling code'''
    def import_structure(self, sbuffer: 'WsiBuffer') -> 'WsiStructure':
        self.struct_buffer.set_buffer_by_buffer(sbuffer.get_buffer_len(self.struct_size))
        return self

    def export_structure(self, sbuffer: 'WsiBuffer'):
        sbuffer.put_byte_ary_d_type(self.struct_buffer.get_buffer(), self.struct_size)
