import base64
import json

portal = context.getPortalObject()

request = context.REQUEST
data_chunk = request.get('data_chunk')

data_set = portal.data_set_module.get(dataset)
if data_set is not None:
  decoded = base64.b64decode(data_chunk)
  data_set.setDescription(decoded)
  response = { 'status_code': 0, 'message': 'Dataset description successfully set.' }
else:
  message = "No remote dataset found for reference '%s'" % (dataset)
  response = { 'status_code': 1, 'message': message }
  context.logEntry(message)

return json.dumps(response)
