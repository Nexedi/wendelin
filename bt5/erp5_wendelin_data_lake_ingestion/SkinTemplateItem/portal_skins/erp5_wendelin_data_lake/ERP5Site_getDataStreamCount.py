"""
This script is called from ebulk client to get count of Data Streams for a Data set.
"""
from erp5.component.module.Log import log

portal = context.getPortalObject()

try:
  data_set = portal.data_set_module.get(data_set_reference)
  if data_set is None or data_set.getReference().endswith("_invalid"):
    return { "status_code": 0, "result": 0 }
except Exception as e:
  log("Unauthorized access to getDataStreamList: " + str(e))
  return { "status_code": 1, "error_message": "401 - Unauthorized access. Please check your user credentials and try again." }

data_stream_list = data_set.DataSet_getDataStreamList()

return { "status_code": 0, "result": len(data_stream_list) }
