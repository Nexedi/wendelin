from slapos import slap

selenium_SR_url = "~/srv/project/slapos/software/headlesschrome-seleniumserver/software.cfg"

my_slap = slap.slap()

my_slap.initializeConnection('https://panel.rapid.space/') #config['master_url'] #doc: slapgrid_uri – uri the slapgrid server connector
# Slapos Master Url: EMPTY (the process uses https://slap.vifib.com/ by default)
# https://panel.rapid.space/ is probably better

computer = my_slap.registerComputer('slaprunner') #config['computer_id'] #doc: computer_guid – the identifier of the computer inside the slapgrid server. #slaprunner?

computer.getComputerPartitionList()

#my_slap.registerSupply().supply(path, computer_guid=config['computer_id'])

my_slap.registerOpenOrder().request( #code: request(self, software_release, partition_reference ...
  path, # SR path
  partition_reference='my_instance')

my_slap.registerOpenOrder().request(selenium_SR_url, 'my_selenium_server')
