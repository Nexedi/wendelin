"""
Get list of Data Streams for context Data set.
"""
data_set_uid = context.getUid()
return context.getDataStreamsByDataSet(data_set_uid, limit)
