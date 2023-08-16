import json
import msgpack

def decodeMSgPack(input_string):
  input_string = input_string.replace("'", "\"")
  input_dict = json.loads(input_string)
  serialized_data = msgpack.packb(input_dict)
  deserialized_data = msgpack.unpackb(serialized_data, raw=False)
  return deserialized_data
