import binascii
import numpy as np
import struct
from cStringIO import StringIO

MAGIC_HEADER = b'\x92WEN\x00\x01'

io = StringIO()
np.save(io, array)
io.seek(0)
npy_data = io.read()
io.close()

crc = struct.pack('<I', binascii.crc32(npy_data) & 0xffffffff)
return b''.join([MAGIC_HEADER, crc, npy_data])
