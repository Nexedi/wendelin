import json

portal = context.getPortalObject()
data = "".join([str(c[1]) for c in context.unpack(data_chunk)])
context.log(type(data))

new_data = context.decodeMSgPack(data)
context.log(type(new_data))

data = data.replace("'", "\"")
data = json.loads(data)
title = data["topic"]
payload = data["payload"]

mqtt_message = portal.mqtt_message_module.newContent(
    portal_type="MQTT Message",
    title=title,
    payload=payload
)
