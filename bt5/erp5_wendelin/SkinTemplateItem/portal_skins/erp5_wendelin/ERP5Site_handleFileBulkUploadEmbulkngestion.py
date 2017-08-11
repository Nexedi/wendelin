"""
  Example script for embulk file upload.
  Each file is saved a new Data Stream object.
"""
from DateTime import DateTime
import string

now = DateTime()
request = context.REQUEST

reference = request.get('reference')
data_chunk = request.get('data_chunk')

#context.log(reference)
#context.log(data_chunk)
if data_chunk is not None and reference is not None:
  data_stream = context.portal_catalog.getResultValue(
                          portal_type = 'Data Stream',
                          reference = reference,
                          validation_state = 'validated')
  if data_stream is None:
    data_stream = context.data_stream_module.newContent(
                            version = '001',
                            portal_type = 'Data Stream',
                            reference = reference)
    data_stream.validate()

  # update data and set sort index and start_date
  data_stream.setData(data_chunk)

  context.log("Saved %s" %data_stream.getPath())

return data_stream.getPath()
