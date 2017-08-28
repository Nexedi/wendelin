"""
  Script that is called before data is appended to a DataStream. This script adds
  the DataStream to the list of objects in the TransactionalVariable that should not be reindexed.
"""
data_stream = state_change['object']
data_stream.DataStream_appendToTransactionalVariable('explicitly_deny_object_reindexation_list', data_stream)
