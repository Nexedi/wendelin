##############################################################################
#
# Copyright (c) 2002-2023 Nexedi SA and Contributors. All Rights Reserved.
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsibility of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# guarantees and support are strongly adviced to contract a Free Software
# Service Company
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
##############################################################################

import string
import random
import urllib
import msgpack

from httplib import NO_CONTENT
from cStringIO import StringIO
from App.version_txt import getZopeVersion
from Products.ERP5Type.tests.ERP5TypeTestCase import ERP5TypeTestCase


if getZopeVersion() < (4, ):
  NO_CONTENT = 200


def getRandomString():
  return "test.%s" %"".join([random.choice(string.ascii_letters + string.digits) for _ in xrange(32)])


class TestDataIngestion(ERP5TypeTestCase):

  """
  Test Class for Data Ingestion via MQTT
  """

  def getTitle(self):
    return "Wendelin Data Ingestion Test for MQTT"


  def test_IngestionFromMQTT(self):

    """
    Test ingestion using a POST Request containing a
    msgpack encoded message simulating input from MQTT.
    """

    topic = getRandomString()
    message1 = getRandomString()
    message2 = getRandomString()

    # Get ingestion policy, data supply and data product
    ingestion_policy = self.portal.portal_ingestion_policies.default_mqtt
    data_supply = self.portal.data_supply_module.default_mqtt
    data_product = self.portal.data_product_module.default_mqtt

    payload = {
      "message1": message1,
      "message2": message2
    }

    data_chunk = {
      "topic": topic,
      "payload": payload
    }

    body = msgpack.packb([0, data_chunk], use_bin_type=True)
    env = { "CONTENT_TYPE": "application/x-www-form-urlencoded" }
    body = urllib.urlencode({ "data_chunk": body })

    path = ingestion_policy.getPath() + "/ingest?reference=" + data_supply.getReference() + "." + data_product.getReference()
    publish_kw = dict(user="ERP5TypeTestCase", env=env, request_method="POST", stdin=StringIO(body))
    response = self.publish(path, **publish_kw)

    # Assert the response status codes
    self.assertEqual(NO_CONTENT, response.getStatus())
    self.tic()

    # Get the latest MQTT Message
    mqtt_message = self.portal.portal_catalog.getResultValue(portal_type="MQTT Message", title=topic)

    # Assert the topic and the payload
    self.assertEqual(mqtt_message.getTitle(), topic)
    self.assertEqual(mqtt_message.getPayload(), str(payload))


  def test_IngestionWithInvalidPolicy(self):

    """
    Test ingestion using an invalid ingestion policy.
    """

    topic = getRandomString()
    message1 = getRandomString()
    message2 = getRandomString()

    # Use an invalid ingestion policy
    # Get data supply and data product
    invalid_policy = "invalid_policy_name"
    data_supply = self.portal.data_supply_module.default_mqtt
    data_product = self.portal.data_product_module.default_mqtt

    payload = {
        "message1": message1,
        "message2": message2
    }

    data_chunk = {
        "topic": topic,
        "payload": payload
    }

    body = msgpack.packb([0, data_chunk], use_bin_type=True)
    env = {"CONTENT_TYPE": "application/x-www-form-urlencoded"}
    body = urllib.urlencode({"data_chunk": body})

    path = invalid_policy + "/ingest?reference=" + data_supply.getReference() + "." + data_product.getReference()
    publish_kw = dict(user="ERP5TypeTestCase", env=env, request_method="POST", stdin=StringIO(body))
    response = self.publish(path, **publish_kw)

    # Assert that the response status code indicates an error (e.g., 404 for not found)
    self.assertEqual(404, response.getStatus())
    self.tic()


  def test_MultipleIngestions(self):

    """
    Test multiple data ingestion requests in succession.
    """

    topic1 = getRandomString()
    message1 = getRandomString()

    topic2 = getRandomString()
    message2 = getRandomString()

    ingestion_policy = self.portal.portal_ingestion_policies.default_mqtt
    data_supply = self.portal.data_supply_module.default_mqtt
    data_product = self.portal.data_product_module.default_mqtt

    payload1 = {
        "message1": message1
    }

    payload2 = {
        "message2": message2
    }

    data_chunk1 = {
        "topic": topic1,
        "payload": payload1
    }

    data_chunk2 = {
        "topic": topic2,
        "payload": payload2
    }

    body1 = msgpack.packb([0, data_chunk1], use_bin_type=True)
    body2 = msgpack.packb([0, data_chunk2], use_bin_type=True)
    env = {"CONTENT_TYPE": "application/x-www-form-urlencoded"}
    body1 = urllib.urlencode({"data_chunk": body1})
    body2 = urllib.urlencode({"data_chunk": body2})

    path = ingestion_policy.getPath() + "/ingest?reference=" + data_supply.getReference() + "." + data_product.getReference()
    publish_kw = dict(user="ERP5TypeTestCase", env=env, request_method="POST", stdin=StringIO(body1))
    response1 = self.publish(path, **publish_kw)

    publish_kw["stdin"] = StringIO(body2)
    response2 = self.publish(path, **publish_kw)

    # Assert the response status codes for both requests
    self.assertEqual(NO_CONTENT, response1.getStatus())
    self.assertEqual(NO_CONTENT, response2.getStatus())
    self.tic()

    # Get the latest MQTT Messages
    mqtt_message1 = self.portal.portal_catalog.getResultValue(portal_type="MQTT Message", title=topic1)
    mqtt_message2 = self.portal.portal_catalog.getResultValue(portal_type="MQTT Message", title=topic2)

    # Assert the topics and payloads for both messages
    self.assertEqual(mqtt_message1.getTitle(), topic1)
    self.assertEqual(mqtt_message1.getPayload(), str(payload1))
    self.assertEqual(mqtt_message2.getTitle(), topic2)
    self.assertEqual(mqtt_message2.getPayload(), str(payload2))
