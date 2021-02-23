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

data_set_uid = data_set.getUid()
data_stream_list = context.getDataStreamsByDataSet(data_set_uid)

'''catalog_kw = {'portal_type': 'Data Ingestion Line',
              'aggregate_uid': data_set_uid
              }
data_ingestion_line_list = context.portal_catalog(**catalog_kw)
data_ingestion_uid_list = [x.getUid() for x in data_ingestion_line_list]

data_stream_list = context.getPortalObject().portal_catalog(
  portal_type="Data Stream",
  aggregate__related__uid=data_ingestion_uid_list
)'''

return { "status_code": 0, "result": len(data_stream_list) }
