portal = context.getPortalObject()

context.log(data_chunk)

mqtt_message = portal.mqtt_message_module.newContent(
  portal_type = "MQTT Message",
  title="test_topic",
  payload="test_payload"
)
