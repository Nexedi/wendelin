REPLACE INTO
  data_stream (uid, set_uid, size, version)
VALUES
<dtml-in prefix="loop" expr="_.range(_.len(uid))">
(
  <dtml-sqlvar expr="uid[loop_item]" type="int">,
  <dtml-sqlvar expr="DataStream_getSetUid[loop_item]" type="int" optional>,
  <dtml-sqlvar expr="getSize[loop_item]" type="string" optional>,
  <dtml-sqlvar expr="getVersion[loop_item]" type="string" optional>
)
<dtml-if sequence-end><dtml-else>,</dtml-if>
</dtml-in>