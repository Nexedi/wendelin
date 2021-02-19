SELECT catalog.uid, catalog.reference, data_stream.size, data_stream.version
FROM catalog AS `catalog`
INNER JOIN
(
  SELECT * FROM data_stream WHERE uid IN
  (
    SELECT DISTINCT catalog.uid FROM
    (
      catalog AS `catalog`
      INNER JOIN
        item AS `item`
      ON
        `item`.`aggregate_uid` = `catalog`.`uid`
    )
    WHERE item.uid IN (
      SELECT * FROM
      (
          SELECT uid
          FROM item
          WHERE aggregate_uid = <dtml-sqlvar data_set_uid type="int">
      ) AS subquery
    )
    AND catalog.portal_type = "Data Stream"
  )
) AS `data_stream`
ON `data_stream`.`uid` = `catalog`.`uid`