import os
import io
import struct
import builtins


from collections import namedtuple

chunk_info_names = ('signature','size','align','skip','start','datapos')

ChunkInfo = namedtuple('ChunkInfo', chunk_info_names)



class FORMReader:
    def __init__(self, stream):
        self._stream = stream
        self._chunks = list()

        # seek to end of stream and save position (stream size)
        self._stream.seek(0, 2)
        size = self._stream.tell()

        # seek to begin of stream and try to read ilff header
        self._stream.seek(0, 0)
        temp = struct.unpack('=4s1H2B4s', self._stream.read(12))

        self._signature = (temp[0])
        self._formatsig = (temp[4]) 
        self._size      = (temp[1]+temp[2])*256+temp[3]

        assert self._signature == b'FORM', "signature must be b'FORM'"
        assert self._formatsig == b'MTP ', "f.signature must be b'MTP'"
        assert self._size+4+4  == size   , "wrong size"
        

 # Reading Bytes Data ->


        while ( self._stream.tell() != size ):
            
            chunk_start = self._stream.tell()

            temp = struct.unpack('=4s1H2B', self._stream.read(8))

            chunk_signature  = (temp[0])
            chunk_size       = (temp[1]+temp[2])*256+temp[3]

            chunk_datapos = self._stream.tell()

            self._stream.seek(self._stream.tell()+chunk_size,0)

            self._chunks.append((chunk_signature,chunk_size,4,chunk_size,chunk_start,chunk_datapos))
            

# Functions


    def close(self):
        self._stream.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    def __del__(self):
        self.close()

    def signatures(self):
        return [item[0] for item in self._chunks]

    def find(self, chunk_signature):
        return chunk_signature in self.signatures()

    def seek(self, chunk_signature, skipone=False):
        skiped = False

        for item in self._chunks:
            if item[0] == chunk_signature:
                if skipone:
                    if not skiped:
                        skiped = True
                        continue

                self._stream.seek(item[5])
                return item


    def read(self, chunk_signature, skipone=False):
        chunk_info = self.seek(chunk_signature, skipone)

        if chunk_info:
            return self._stream.read(chunk_info[1])


    def info(self, chunk_signature, skipone=False):
        skiped = False

        for item in self._chunks:
            if item[0] == chunk_signature:
                if skipone:
                    if not skiped:
                        skiped = True
                        continue

                return ChunkInfo(item)


def open(file, mode=None):
    if isinstance(file, str):
        return FORMReader(builtins.open(file, 'rb'))
    elif isinstance(file, io.BytesIO):
        return FORMReader(file)
    else:
        raise ValueError("file expected str or BytesIO")
