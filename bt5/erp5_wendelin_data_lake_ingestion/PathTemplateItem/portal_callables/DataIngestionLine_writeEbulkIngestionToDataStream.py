import hashlib
import base64

CHUNK_SIZE = 200000

def getHash(data_stream):
  hash_md5 = hashlib.md5()
  data_stream_chunk = None
  n_chunk = 0
  chunk_size = CHUNK_SIZE
  while True:
    start_offset = n_chunk*chunk_size
    end_offset = n_chunk*chunk_size+chunk_size
    try:
      data_stream_chunk = ''.join(data_stream.readChunkList(start_offset, end_offset))
    except Exception:
      # data stream is empty
      data_stream_chunk = ""
    hash_md5.update(data_stream_chunk)
    if data_stream_chunk == "": break
    n_chunk += 1
  return hash_md5.hexdigest()

decoded = base64.b64decode(data_chunk)
data_stream.appendData(decoded)
data_stream.setVersion(getHash(data_stream))
