"""
This script is called from ebulk client to get list of Data Streams for a Data set.
"""
import json
from erp5.component.module.Log import log

portal = context.getPortalObject()

try:
  data_set = portal.data_set_module.get(data_set_reference)
  # XXX: why does we need reference= "something_invalidated" when we have Data Set's state ?
  if data_set is None or data_set.getReference().endswith("_invalid"):
    return { "status_code": 0, "result": [] }
except Exception as e: # fails because unauthorized access
  log("Unauthorized access to getDataStreamList: " + str(e))
  return { "status_code": 1, "error_message": "401 - Unauthorized access. Please check your user credentials and try again." }

data_stream_dict = {}
# XXX: reference NOT ending with "_invalidated" -> why is that needed when we can invalidate Data Stream ???
# XXX: state != draft
catalog_kw = dict(portal_type = "Data Stream", 
                  set_uid = data_set.getUid(),
                  #limit=[1000, 20], # XXX: add new script arguments start and offset to script and make ebulk use them!
                  sort_on=(("creation_date", "ascending",),),
                  validation_state = ['published', 'validated'])
data_stream_brain_list = portal.portal_catalog(**catalog_kw)
context.log("Data Streams found=%s" %len(data_stream_brain_list))

for stream_brain in data_stream_brain_list:
  reference = stream_brain.getReference()
  version = stream_brain.version
  size = stream_brain.size
  data_stream_id = "data_stream_module/%s" %stream_brain.id
  #context.log("id=%s, version=%s, reference=%s, size=%s" %(data_stream_id, version, reference, size))
  data_stream_info_dict = {'id': data_stream_id,
                           'size': size,
                           'hash': version}
  if reference in data_stream_dict:
    data_stream_dict[reference]['data-stream-list'].append(data_stream_info_dict)
    data_stream_dict[reference]['large-hash'] = data_stream_dict[reference]['large-hash'] + str(version)
    data_stream_dict[reference]['full-size'] = int(data_stream_dict[reference]['full-size']) + int(size)
  else:
    data_stream_dict[reference] = { 'data-stream-list': [data_stream_info_dict],
                                    'id': data_stream_id,
                                    'reference': reference,
                                    'large-hash': version,
                                    'full-size': size}

result_dict = { 'status_code': 0, 'result': data_stream_dict.values()}
return json.dumps(result_dict)
