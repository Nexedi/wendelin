"""
Each Data Stream can be grouped in a logical set with a dedicated portal type which represents the set.

For ebulk this portal type is "Data Set" but in theory it can be anything. Thus name of script is intentionally using 'Set'.

This script works for the  default ingestion model used by ebulk:
- Data Ingestion
  - Data Ingestion Line
     (aggregate) -> Data Stream
     (aggregate) -> Date Set

Note: for this to work we must working an index relation between Data Ingestion Line and Data Stream!  
"""
data_stream = context.getObject()
data_ingestion_line = data_stream.portal_catalog.getResultValue(
                        portal_type = "Data Ingestion Line", 
                        aggregate_uid = context.getObject().getUid())
#context.log("DS=%s , DI=%s" %(data_stream, data_ingestion_line))
if data_ingestion_line is not None:
  #context.log(data_ingestion_line.getRelativeUrl())
  data_set = data_ingestion_line.getAggregateValue(portal_type = "Data Set")
  if data_set is not None:
    #context.log("set_uid=%s" %data_set.getUid())
    return data_set.getUid()
