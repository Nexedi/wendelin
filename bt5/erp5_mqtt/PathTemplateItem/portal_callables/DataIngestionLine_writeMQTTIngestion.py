import json

portal = context.getPortalObject()
data = "".join([str(c[1]) for c in context.unpack(data_chunk)])
deserialized_data = context.Base_decodeMSgPack(data)
title = deserialized_data["topic"]
payload = deserialized_data["payload"]

mqtt_message = portal.mqtt_message_module.newContent(
    portal_type="MQTT Message",
    title=title,
    payload=payload
)
