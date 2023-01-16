#!//usr/bin/python
# -*- coding: utf-8 -*-

import base64
import requests
import os

# configure for your instance
ing_policy = "drone_simulation"
# more hierarchy like run1.log1 which involve new developments on wendelin side (ingest/parse/operation scripts)
reference = "drone_simulation"
username = "zope"
password = "roque"
ingestion_policy_url = "https://softinst178934.host.vifib.net/erp5/portal_ingestion_policies/%s/ingest" %(ing_policy)

log_dir = "./logs/"
log_dir = "./logs-simple/"
dir_list = os.listdir(log_dir)
for d in dir_list:
  data = ""
  file_list = os.listdir(log_dir + d)
  for f in file_list:
    file = open(log_dir + d + "/" + f)
    data += "%s-%s:\n" % (str(d), str(f)) + file.read() + "\n"
  data += "#"
  data_bytes = data.encode("utf-8")
  base64_bytes = base64.b64encode(data_bytes)
  base64_string = base64_bytes.decode("utf-8")
  params = {'reference': reference,
            'data_chunk': base64_string}
  headers = {'CONTENT_TYPE': 'application/octet-stream'}
  pass
  r = requests.post(ingestion_policy_url,
                    params = params,
                    headers=headers,
                    auth=(username, password))
  if r.status_code >= 200 and r.status_code<=204:
    print("Successfully uploaded  %s bytes to Wendelin. " %len(data))
  else:
    print("url request error:" + str(r.status_code))
    print(r.text)
    print(r.headers)
    print(r.reason)
