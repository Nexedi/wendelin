portal = context.getPortalObject()

INVALID_SUFFIX = portal.DataLake_getIngestionReferenceDictionary()["invalid_suffix"]

return document.getReference().endswith(INVALID_SUFFIX)
