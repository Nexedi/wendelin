#!//usr/bin/python
# -*- coding: utf-8 -*-
"""
Sample Python script to ingest into a Wendelin instance.
"""

import msgpack
import requests

# configure for your instance parameters below
reference = ""
username = ""
password = ""
ingestion_policy_url = "https://%s:%s@....../erp5/portal_ingestion_policies/...../ingest" %(username, password)

data = {"msg": 'Hello World! Zdravej Sviat!'}
payload = msgpack.packb([0, data], use_bin_type=True)

params = {'reference': reference,
          'data_chunk': payload}
headers = {'CONTENT_TYPE': 'application/octet-stream'}

r = requests.post(ingestion_policy_url, 
                  params = params, 
                  headers=headers)
print "Response=%s" %r.status_code