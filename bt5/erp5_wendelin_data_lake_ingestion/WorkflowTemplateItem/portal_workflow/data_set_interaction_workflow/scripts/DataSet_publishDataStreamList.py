"""
  Publish all Data Streams for a Data Set.
"""
data_set = state_change['object']
for data_stream in data_set.DataSet_getDataStreamList():
  try:
    data_stream.activate().publish()
  except:
    #ignore draft data streams or corresponding to old invalidated ingestions
    pass
