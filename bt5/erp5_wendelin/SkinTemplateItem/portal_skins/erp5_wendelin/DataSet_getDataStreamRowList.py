"""
Get list of Data Streams for context Data set.
"""
data_set_uid = context.getUid()

catalog_kw = {'portal_type': 'Data Ingestion Line',
              'aggregate_uid': data_set_uid,
              'limit': limit,
              }
data_ingestion_line_list = context.portal_catalog(**catalog_kw)
data_ingestion_uid_list = [x.getUid() for x in data_ingestion_line_list]

return context.getPortalObject().portal_catalog(
  portal_type="Data Stream",
  aggregate__related__uid=data_ingestion_uid_list,
  select_list=['reference', 'relative_url', 'data_stream.size', 'data_stream.version'],
)
