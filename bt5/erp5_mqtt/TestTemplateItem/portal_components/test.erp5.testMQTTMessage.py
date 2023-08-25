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

import urllib
import msgpack

from httplib import NO_CONTENT
from cStringIO import StringIO
from App.version_txt import getZopeVersion
from Products.ERP5Type.tests.ERP5TypeTestCase import ERP5TypeTestCase


if getZopeVersion() < (4, ):
  NO_CONTENT = 200


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

    ingestion_policy = self.portal.portal_ingestion_policies.default_mqtt

    data_chunk = {
      "topic": "test_sensor.test_product",
      "payload": {
        "message1": "Hello, World!",
        "message2": "Hello, World Again!"
      }
    }

    body = msgpack.packb([0, data_chunk], use_bin_type=True)
    env = {"CONTENT_TYPE": "application/x-www-form-urlencoded"}
    body = urllib.urlencode({"data_chunk": body})

    path = ingestion_policy.getPath() + "/ingest?reference=test_sensor.test_product"
    publish_kw = dict(user="ERP5TypeTestCase", env=env, request_method="POST", stdin=StringIO(body))
    response = self.publish(path, **publish_kw)

    self.assertEqual(NO_CONTENT, response.getStatus())
    self.tic()
