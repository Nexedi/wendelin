"""
  Invalidate all Data Streams for a Data Set.
"""
data_set = state_change['object']
for data_stream in data_set.DataSet_getDataStreamList():
  if data_stream and data_stream.getValidationState() != 'draft':
    data_stream.activate().invalidate()
