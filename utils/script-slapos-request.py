import time
#from slapos import request

NUMBER_OF_SERVERS = 2

selenium_SR_url = "~/srv/project/slapos/software/seleniumserver/software.cfg"
selenium_SR_url = "~/srv/project/slapos/software/seleniumrunner/software.cfg"
selenium_SR_url = "/srv/slapgrid/slappart6/srv/project/slapos/software/seleniumserver/software.cfg"

instance_list = []

for i in range(NUMBER_OF_SERVERS):
  instance = request(selenium_SR_url, "seleniumserver-" + str(i))
  instance_list.append(instance)

done = False
nap = 300
while not done:
  for instance in instance_list:
    print("checking instance in %s" % instance.getId())
    print("instance started?")
    if instance.getState() != 'started':
      print("instance NOT started")
      time.sleep(nap)
      break
    print("instance started!")
    print("instance ready?")
    try:
      instance.getConnectionParameter('url')
    except:
      print("instance NOT ready")
      time.sleep(nap)
      break
    print("instance in %s ready!" % instance.getId())
  done = True

print("all instance ready")

server_url_list = []

print("Server urls:")

for instance in instance_list:
  # get a specific parameter info
  server_url = instance.getConnectionParameter('url')
  server_url_list.append(server_url)
  print(server_url)
  # e.g. 'https://selenium:jvT0SRR9Mtad@[2001:67c:1254:5f:d58a::5933]:9443/wd/hub'
  #instance.getConnectionParameter('connection-parameters')
  # ?? ERROR, not found


#OUTSIDE (slapos console)
#slapos service list
#{
#  "seleniumserver": "~/srv/project/slapos/software/seleniumserver/software.cfg"
#}

#slapos service info seleniumserver
# dict with all info