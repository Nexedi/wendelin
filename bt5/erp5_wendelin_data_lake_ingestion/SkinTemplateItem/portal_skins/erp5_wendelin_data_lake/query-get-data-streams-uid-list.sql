#query 1
#get data ingestion line uid list for dataset "test_dataset" (ds uid: 16376)
#select * from item where aggregate_uid = 16376

#query 2
#get data stream uid list for previous DIL list
SELECT DISTINCT catalog.uid as "catalog uid", catalog.path, catalog.portal_type, item.uid as "item uid", item.aggregate_uid as "item aggregate_uid" FROM
  (
    catalog AS `catalog`
  INNER JOIN
    item AS `item`
  ON
    `item`.`aggregate_uid` = `catalog`.`uid`
  )
  where
  item.uid in (16378)
  #problem with list argument: type is required and only allows string, int, float and no-blank
  #item.uid in <dtml-sqlvar data_ingestion_line_uid_list type="string">
  and catalog.portal_type = "Data Stream"

#query 3
#get data stream full info from new table data_stream
#select * from data_stream where uid in (16377) #this should be the DS uid list from query 2