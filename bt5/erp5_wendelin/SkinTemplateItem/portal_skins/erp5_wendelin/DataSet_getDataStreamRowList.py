portal = context.getPortalObject()

catalog_kw = dict(portal_type = "Data Stream",
                  set_uid = context.getUid(),
                  limit=limit,
                  sort_on=(("creation_date", "ascending",),),
                  validation_state = ['published', 'validated'])
data_stream_brain_list = portal.portal_catalog(**catalog_kw)
return data_stream_brain_list
