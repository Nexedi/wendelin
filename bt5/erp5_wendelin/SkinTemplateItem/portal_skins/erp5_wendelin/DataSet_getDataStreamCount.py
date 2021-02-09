"""
Get count of Data Streams for context Data set.
"""
portal = context.getPortalObject()

catalog_kw = dict(portal_type = "Data Stream",
                  set_uid = context.getUid(),
                  validation_state = ['published', 'validated'])
return len(portal.portal_catalog(**catalog_kw))
