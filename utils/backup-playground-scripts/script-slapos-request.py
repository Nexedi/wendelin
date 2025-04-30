import time
from slapos import slap

NUMBER_OF_SERVERS = 2

selenium_SR_url = "~/srv/project/slapos/software/seleniumserver/software.cfg"
#TODO how to get SR url?
selenium_SR_url = "/srv/slapgrid/slappart70/srv/project/slapos/software/headlesschrome-seleniumserver/software.cfg"

print("REQUESTING SERVER INSTANCES")

my_slap = slap.slap()
#TODO how to get master_url?
my_slap.initializeConnection('http://10.0.222.95:4000') #slapgrid_uri – uri the slapgrid server connector

instance_list = []

for i in range(NUMBER_OF_SERVERS):
  instance = my_slap.registerOpenOrder().request(selenium_SR_url, "headlesschrome-seleniumserver-" + str(i))
  instance_list.append(instance)
  print("instance requested: %s" % instance.getId())

done = False
nap = 300
while not done:
  done = True
  for instance in instance_list:
    print("checking instance in %s" % instance.getId())
    print("instance started?")
    if instance.getState() != 'started':
      print("instance NOT started")
      time.sleep(nap)
      done = False
      continue
    print("instance started!")
    print("instance ready?")
    try:
      instance.getConnectionParameter('frontend-url')
    except:
      print("instance NOT ready")
      time.sleep(nap)
      done = False
      continue
    print("instance in %s ready!" % instance.getId())

print("all instances ready")

server_url_list = []

print("Server urls:")

for instance in instance_list:
  # get a specific parameter info
  server_url = instance.getConnectionParameter('frontend-url')
  server_url_list.append(server_url)

print(server_url_list)
