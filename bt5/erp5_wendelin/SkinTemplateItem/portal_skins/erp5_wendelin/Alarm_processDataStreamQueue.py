portal = context.getPortalObject()
activate = portal.portal_activities.activateObject
for x in portal.Alarm_zDataStreamQueue():
  activate(x.path, tag=tag,
    serialization_tag='process_data_stream:%s' % x.uid
  ).processDataStreamQueue()
