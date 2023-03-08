import time
from slapos import request

selenium_SR_url = "~/srv/project/slapos/software/seleniumserver/software.cfg"
selenium_SR_url = "~/srv/project/slapos/software/seleniumrunner/software.cfg"
selenium_SR_url = "/srv/slapgrid/slappart6/srv/project/slapos/software/seleniumserver/software.cfg"
# TODO: request 2 or more instances
instance = request(selenium_SR_url, "seleniumserver")
instance = request(selenium_SR_url, "selenium-server-roque")
instance = request(selenium_SR_url, "seleniumrunner")

done = False
nap = 300
while not done:
  #TODO iterate instances
  print("instance started?")
  if instance.getState() != 'started':
    print("instance NOT started")
    time.sleep(nap)
    continue
  print("instance started!")
  print("instance ready?")
  try:
    instance.getConnectionParameter('url')
  except:
    print("instance NOT ready")
    time.sleep(nap)
    continue
  print("instance ready!")
  done = True

server_url = instance.getConnectionParameter('url')
print("server_url:")
print(server_url)

# get a specific parameter info
instance.getConnectionParameter('url')
# 'https://selenium:jvT0SRR9Mtad@[2001:67c:1254:5f:d58a::5933]:9443/wd/hub'

instance.getConnectionParameter('connection-parameters')
# ?? ERROR, not found

#OUTSIDE (slapos console)
#slapos service list
#{
#  "seleniumserver": "~/srv/project/slapos/software/seleniumserver/software.cfg"
#}

#slapos service info seleniumserver
# dict with all info