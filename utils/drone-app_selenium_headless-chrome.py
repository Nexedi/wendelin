import sys
import time
import itertools
import certifi
import urllib3
from slapos import slap
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.remote.remote_connection import RemoteConnection
from datetime import datetime

##### SERVER INSTANCES REQUEST #####

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
  reference = "headlesschrome-seleniumserver-" + str(i)
  instance = my_slap.registerOpenOrder().request(selenium_SR_url, reference)
  instance_list.append(instance)
  print("instance %s requested at %s" % (reference, instance.getId()))

done = False
nap = 300
while not done:
  done = True
  for instance in instance_list:
    print("checking instance in %s" % instance.getId())
    if instance.getState() != 'started':
      time.sleep(nap)
      done = False
      continue
    try:
      instance.getConnectionParameter('frontend-url')
    except:
      print("instance NOT ready")
      time.sleep(nap)
      done = False
      continue
    print("instance in %s ready!" % instance.getId())

server_url_list = []

for instance in instance_list:
  frontend_url = instance.getConnectionParameter('frontend-url')
  protocol = frontend_url.split('//')[0]
  domain = frontend_url.split('//')[1]
  user = instance.getConnectionParameter('user')
  pswrd = instance.getConnectionParameter('pass')
  server_url = "%s//%s:%s@%s" % (protocol, user, pswrd, domain)
  server_url_list.append(server_url)

print("All instances ready. Server url list:")
print(server_url_list)

##### DRONE SIMULATION RUN #####

DEBUG = True

NUMBER_OF_DRONES = 1
GRANULARITY = 2
GAME_INPUT_ID_LIST=["simulation_speed", "simulation_time", "number_of_drones", "drone_min_speed", "drone_max_speed", "drone_max_acceleration", "drone_max_deceleration", "start_AMSL", "init_pos_lat", "init_pos_lon", "init_pos_z", "drone_max_sink_rate", "drone_max_climb_rate"]
GAME_INPUT_VALUE_LIST=[1500*60, 1500, NUMBER_OF_DRONES, 12, 20, 6, 1, "594.792", "45.6403", "14.2648", "65.668", 3, 8]
#DRONE_INPUT_ID_LIST=["drone_speed", "drone_max_roll", "drone_min_pitch", "drone_max_pitch"]
#DRONE_VALUE_RANGE_LIST=[[12, 20], [10, 50], [-35, -10], [10, 40]]
DRONE_INPUT_ID_LIST=["drone_speed", "drone_min_speed"]
DRONE_VALUE_RANGE_LIST=[[10, 20], [5, 10]]
DRONE_INPUT_VALUE_LIST=[]
AI_SCRIPT = ""
if (len(sys.argv)>1):
  AI_SCRIPT = open(sys.argv[1], "r").read().replace("\n", "\\n").replace('"', "'")
REMOTE = True # flag to set if run remote or local
APP_URL = "https://dronesimulator.app.officejs.com/"
EMPTY_URL = "data:,"
#server_url_list = [
#  "https://selenium:i1Kzu0Yd8L2R@softinst183023.host.vifib.net",
#  "https://selenium:dBlhn3DRcpgu@softinst183024.host.vifib.net"
#]

##### FUNCTIONS DEFINITION #####

# UTILS

def takeFullScreenshot(driver, filename):
  driver.set_window_size(1000, 3080)
  driver.get_screenshot_as_file(filename)
  driver.set_window_size(800, 600)
  return
  if not DEBUG:
    return
  try:
    S = lambda X: driver.execute_script('return document.body.parentNode.scroll'+X)
    driver.set_window_size(S('Width'),S('Height')*1.5) # May need manual adjustment
    body = driver.find_element_by_tag_name('body')
    body.screenshot(filename)
  except Exception as e:
    # take the screenshot in the standard way
    driver.set_window_size(1000, 3080)
    driver.get_screenshot_as_file(filename)

def values_in_range(start, end, n):
  if n == 1:
    return [start]
  d = (end - start) / (n - 1)
  return [start + i*d for i in range(n)]

# WEB DRIVER PROCESS

def createDriver(server_url, options):
  print("Creating webdriver for " + server_url)
  done = False
  retry = 0
  while not done:
    if retry == 10:
        raise RuntimeError("Error: couldn't create webdriver after 10 attempts for " + server_url)
    try:
      if (REMOTE):
        driver = webdriver.Remote(
            command_executor=server_url,
            desired_capabilities=options.to_capabilities()
        )
      else: # local selenium
        driver = webdriver.Chrome(options=options, desired_capabilities=options.to_capabilities())
      EMPTY_URL = driver.current_url
      str_version = driver.capabilities['browserVersion'].split('.')[0]
      # create only v91
      if (int(str_version)) != 91:
        raise Exception("Discard non-91 chrome version.")
      print("Webdriver created. Chrome version: " + str_version)
      done = True
    except Exception as e:
      print("Error creating webdriver. Retry.")
      print(e)
      retry += 1
  return driver

def initDriver(driver):
  print("- INIT-DRIVER")
  if driver.current_url == EMPTY_URL:
    #print("driver url empty. calling GET app_url")
    driver.get(APP_URL)
  #else:
    #print("driver url already set, DON'T call GET")
  # skip bootloader
  skip_list = driver.find_elements(By.XPATH, '//a[@class="skip-link" and text()="Skip"]')
  if len(skip_list) > 0:
    #print("skipping bootloader (click on skip)")
    skip_list[0].click()
  #else:
  #  print("skip bootL not found")

def loadDriver(driver):
  print("- LOAD-DRIVER")
  # fill game inputs
  #print("filling common inputs") #this takes time and it's serial (1sec per input)
  for i, input_id in enumerate(GAME_INPUT_ID_LIST):
    input = driver.find_element(By.ID, input_id)
    input.clear()
    input.send_keys(GAME_INPUT_VALUE_LIST[i])

  # fill codemirror editor input
  if (AI_SCRIPT):
    #print("filling AI_SCRIPT")
    frame = driver.find_element(By.XPATH, '//iframe')
    driver.switch_to.frame(frame)
    driver.execute_script('return document.getElementsByClassName("CodeMirror")[0].CodeMirror.setValue("' + AI_SCRIPT + '")')
    driver.switch_to.default_content()
  print("- load done")

def runDriverNew(driver, combination):
  print("- RUN-DRIVER - combination: " + str(combination))
  # fill drone inputs
  for i, input_id in enumerate(DRONE_INPUT_ID_LIST):
    input = driver.find_element(By.ID, input_id)
    input.clear()
    input.send_keys(str(combination[i]))
  #run the simulation
  run_button = driver.find_element(By.XPATH, '//input[@type="submit" and @name="action_run"]')
  run_button.click()
  print("- run clicked")

def reloadDriver(driver):
  print("- RELOAD-DRIVER")
  driver.refresh();
  #print("refresh called")
  driver.get(APP_URL)
  #print("GET app_url called.")

def downloadLogs(driver_dict):
  print("- DOWNLOAD LOGS")
  for i in range(NUMBER_OF_DRONES):
    text = "Download Simulation LOG " + str(i)
    #id_s = "log_result_" + str(i)
    download_log = driver_dict['driver'].find_element(By.XPATH, '//div[@class="container"]//a[contains(text(), "' + text + '")]')
    download_log.click() #saves log txt file in command location
    time.sleep(0.5)
    print("- Clicked - " + text + " - " + driver_dict['id'] + ' - ' + str(driver_dict['running_combination']))
  print("- download logs done")

def initDone(driver):
  iframe_list = driver.find_elements(By.XPATH, '//iframe')
  return len(iframe_list) > 0

def runDone(driver):
  # check error:
  error_list = driver_dict['driver'].find_elements(By.XPATH, '//div[@class="visible"]//button[contains(text(), "Error:")]')
  if (len(error_list) > 0):
    webgl_teximage2d_error = driver_dict['driver'].find_elements(By.XPATH, '//div[@class="visible"]//button[contains(text(), "Failed to execute")]')
    if (len(webgl_teximage2d_error) > 0):
      raise Exception("[ERROR] webgl_teximage2d_error")
    print("- [ERROR] while running - " + error_list[0].text)
    print("- DISCARD invalid combination")
    print("- " + driver_dict['id'] + " set state to draft")
    driver_dict['state'] = 'draft'
    # discard error combination (may be an invalid set of parameters)
    driver_dict['running_combination'] = None
  # check if finished
  link_list = driver.find_elements(By.XPATH, '//div[@class="container"]//a[contains(text(), "Download Simulation LOG")]')
  return len(link_list) > 0

##### MAIN #####

# generate input values
for i in range(len(DRONE_VALUE_RANGE_LIST)):
  DRONE_INPUT_VALUE_LIST.append(values_in_range(DRONE_VALUE_RANGE_LIST[i][0], DRONE_VALUE_RANGE_LIST[i][1], GRANULARITY))

# generate all input combinations
combination_list = [combination for combination in itertools.product(*DRONE_INPUT_VALUE_LIST)]

start_time = datetime.now()
print("Start execution at:")
print(start_time.strftime("%d/%m/%Y %H:%M:%S"))
print("Full combination_list:")
print(combination_list)

# configure the web driver settings
options = webdriver.ChromeOptions()
#options.set_capability("browserVersion", "91.0.4472.0")
options.add_argument('--headless=new')
options.add_argument('--window-size=800x600')
options.add_argument('--incognito')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

# create all drivers
driver_list = []
for idx, server_url in enumerate(server_url_list):
  driver = createDriver(server_url, options)
  driver_dict = {
    'id': 'D' + str(idx),
    'state': 'draft',
    'driver': driver,
    'running_combination': None
  }
  driver_list.append(driver_dict)

creation_time = datetime.now()
creation_elapsed_time = creation_time - start_time

iter = 0
finished_driver_count = 0
while finished_driver_count < len(driver_list):
  for driver_dict in driver_list:
    #print("Checking driver " + str(driver_dict['id']) + ", with state: " + str(driver_dict['state']) + " (has running comb: " + str(driver_dict['running_combination']) + ")")
    driver = driver_dict['driver']
    try:
      if driver_dict['state'] == 'draft':
        print(driver_dict['id'] + " in state draft!")
        initDriver(driver)
        if initDone(driver):
          print(driver_dict['id'] + " init done (iframe found). set state to init")
          driver_dict['state'] = 'init'
      if driver_dict['state'] == 'init':
        print(driver_dict['id'] + " in state init!")
        loadDriver(driver)
        print(driver_dict['id'] + " set state to loading")
        driver_dict['state'] = 'loading'
      if driver_dict['state'] == 'loading':
        print(driver_dict['id'] + " in state loading!")
        if len(combination_list) > 0:
          combination = combination_list.pop()
          driver_dict['running_combination'] = combination
          runDriverNew(driver, combination)
          print(driver_dict['id'] + " set state to running")
          driver_dict['state'] = 'running'
        else:
          print(driver_dict['id'] + " set state to finished")
          driver_dict['state'] = 'finished'
          finished_driver_count += 1
      if driver_dict['state'] == 'running':
        #print(driver_dict['id'] + " in state running!")
        if runDone(driver):
          print(driver_dict['id'] + " run done! donwlog links found")
          downloadLogs(driver_dict)
          #reloadDriver(driver)
          print(driver_dict['id'] + " set state to draft")
          driver_dict['state'] = 'draft'
          driver_dict['running_combination'] = None
          iter += 1
        #else:
        #  print("still running")
    except Exception as e:
      print("ERROR: " + str(e))
      combination_list.append(driver_dict['running_combination'])
      driver_dict['running_combination'] = None
      reloadDriver(driver)
      print("set state to draft")
      driver_dict['state'] = 'draft'

end_time = datetime.now()
print("End execution at:")
print(end_time.now().strftime("%d/%m/%Y %H:%M:%S"))
elapsed_time = end_time - creation_time #start_time
print("Total combinations: " + str(iter))
print("Total time for driver creation: %s seconds. " % str(creation_elapsed_time.seconds))
print("Total time for runs: %s seconds. " % str(elapsed_time.seconds))

print("All drivers quit")