import pandas as pd
import numpy as np

# Function to remove non-ASCII characters from a string, because I can not be bothered to make to_records with utf8 right now
def remove_non_ascii(text):
    return ''.join(char for char in str(text) if ord(char) < 128)


progress_indicator = in_stream["Progress Indicator"]
in_data_stream = in_stream["Data Bucket Stream"]
out_data_array = out_array["Data Array"]

keys = in_data_stream.getKeyList()


start = progress_indicator.getIntOffsetIndex()
# Later we can add a chunk variable, which would tell us how many buckets we can process each call. But currently we do not have many buckets.
end = len(keys)

context.log(in_data_stream)

if end == 0:
  context.log("No Keys found")
  return 


for key in keys[start:end]: # should be start instead of 1, but because we have none in there we do it like this for the broken part
  context.log(key)
  log = in_data_stream.getBucketByKey(key)
  df = pd.read_csv(log, sep=';', dtype=str)
  if df.shape[0] == 0:
    return


  # Remove non-ASCII characters from DataFrame values
  df = df.applymap(remove_non_ascii)

  # Remove non-ASCII characters from column names (headers)
  df.columns = df.columns.map(remove_non_ascii)

# Convert non-numeric columns to float64
  non_numeric_columns = df.select_dtypes(exclude=[np.number]).columns
  df[non_numeric_columns] = df[non_numeric_columns].apply(pd.to_numeric, errors='coerce')



  ndarray = df.to_records(convert_datetime64=False)

  zbigarray = out_data_array.getArray()

  if zbigarray is None:
    zbigarray = out_data_array.initArray(shape=(0,), dtype=ndarray.dtype.fields)

  start_array = zbigarray.shape[0]
  zbigarray.append(ndarray)



  data_array_line = out_array.get(key)

  if data_array_line is None:
    data_array_line = out_data_array.newContent(id=key,
                                             portal_type="Data Array Line")

  data_array_line.edit(reference=key,
       index_expression="%s:%s" %(start_array, zbigarray.shape[0])
    )




  context.log("index_expression")
  context.log("%s:%s" %(start_array, zbigarray.shape[0]))





# This is quite useless currently, as we are able to read all the buckets in one go. But in the case we want to only iterate over one bucket at a time (or a chunk of them) we can use this. 

if end > start:
  progress_indicator.setIntOffsetIndex(end)

if end < len(keys):
  return 1
