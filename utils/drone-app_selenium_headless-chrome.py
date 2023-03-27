import sys
import time
import itertools
import certifi
import urllib3
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.remote.remote_connection import RemoteConnection
from datetime import datetime

DEBUG = False

##### FUNCTIONS DEFINITION #####

def takeFullScreenshot(driver, filename):
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

def setup_driver_on_app(server_url, options, dc):
  print("Creating webdriver for " + server_url)
  done = False
  retry = 0
  while not done:
    if retry == 10:
        raise RuntimeError("Error: couldn't create webdriver after 10 attempts for " + server_url)
    try:
      if (REMOTE):
        # run selenium remote server
        #executor = RemoteConnection(server_url, keep_alive=True)
        #cert_reqs = 'CERT_REQUIRED'
        #ca_certs = certifi.where()
        #executor._conn = urllib3.PoolManager(cert_reqs=cert_reqs, ca_certs=ca_certs)
        driver = webdriver.Remote(
            #command_executor=executor,
            command_executor=server_url,
            desired_capabilities=dc,
        )
      else:
        # local selenium
        driver = webdriver.Chrome(options=options, desired_capabilities=dc)

      # navigate to drone app
      driver.get(APP_URL)
      driver.implicitly_wait(5)
      # skip bootloader
      try:
        skip = driver.find_element(By.XPATH, '//a[@class="skip-link" and text()="Skip"]')
        skip.click()
      except:
        # if app was installed  on a previous run, there is no bootloader page. contine
        pass

      # wait for editor iframe content
      driver.implicitly_wait(20)
      iframe = driver.find_element(By.XPATH, '//iframe')

      # fill game inputs
      for i, input_id in enumerate(GAME_INPUT_ID_LIST):
        input = driver.find_element(By.ID, input_id)
        input.clear()
        input.send_keys(GAME_INPUT_VALUE_LIST[i])

      # fill codemirror editor input
      if (AI_SCRIPT):
        frame = driver.find_element(By.XPATH, '//iframe')
        driver.switch_to.frame(frame)
        driver.execute_script('return document.getElementsByClassName("CodeMirror")[0].CodeMirror.setValue("' + AI_SCRIPT + '")')
        driver.switch_to.default_content()
        #driver.get_screenshot_as_file('ai.png')

      driver.implicitly_wait(0)
      print("Webdriver created.")
      #driver.get_screenshot_as_file('DEBUG-web-driver-created.png')
      done = True
    except Exception as e:
      print("Error creating webdriver.")
      print(e)
      print("retry")
      retry += 1
  return driver

def checkDriver(driver_dict):
  print("Checking driver " + str(driver_dict['id']) + " (has running comb: " + str(driver_dict['running_combination']) + ")")
  try:
    if driver_dict['running_combination']:
      if not driver_dict['first_run']:
        driver_dict['driver'].find_element(By.XPATH, '//div[@class="container"]//a[contains(text(), "Download Simulation LOG")]')
        print("LOG link FOUND")
        txt = 'DEBUG-saving-results-' + driver_dict['id'] + '-' + str(driver_dict['running_combination'])
        print("Driver finished run! " + txt + " (screenshot taken)")
        #driver_dict['driver'].get_screenshot_as_file(txt + '.png')
        #takeFullScreenshot(driver_dict['driver'], txt + '.png')
        for i in range(NUMBER_OF_DRONES):
          text = "Download Simulation LOG " + str(i)
          #id_s = "log_result_" + str(i)
          download_log = driver_dict['driver'].find_element(By.XPATH, '//div[@class="container"]//a[contains(text(), "' + text + '")]')
          download_log.click() #saves log txt file in command location
          time.sleep(1)
          print("DEBUG - " + text + " - " + driver_dict['id'] + '-' + str(driver_dict['running_combination']))
        print("driver ready for another comb. Set it to free")
        driver_dict['running_combination'] = None #free driver
      else:
        print("first run for the driver!")
        driver_dict['first_run'] = False
  except Exception as e:
    print("driver is still busy")
    # check if app failed
    takeFullScreenshot(driver_dict['driver'], 'driver-still-busy.png')
    try:
      error = driver_dict['driver'].find_element(By.XPATH, '//div[@class="visible"]//button[contains(text(), "Failed to execute")]')
      print("")
      print("[ERROR] teximage2d error on comb  " + str(driver_dict['running_combination']) + ". Setting driver free.")
      print("")
      txt = 'DEBUG-error-exception-' + driver_dict['id'] + '-' + str(driver_dict['running_combination'])
      #driver_dict['driver'].get_screenshot_as_file(txt + '.png')
      takeFullScreenshot(driver_dict['driver'], txt + '.png')
      driver_dict['running_combination'] = None #free driver
    except:
      print("not teximage2d error. good.")
      pass
    if driver_dict['print-exception']:
      txt = 'DEBUG-exception-' + driver_dict['id'] + '-' + str(driver_dict['running_combination'])
      #driver_dict['driver'].get_screenshot_as_file(txt + '.png')
      takeFullScreenshot(driver_dict['driver'], txt + '.png')
      print(e)
      print(type(e).__name__)

def getFreeDriver(combination):
  free_driver = None
  for driver_dict in driver_list:
    driver_dict['driver'].implicitly_wait(0)
    checkDriver(driver_dict)
    if not free_driver:
      if not driver_dict['running_combination']:
        driver_dict['running_combination'] = combination
        free_driver = driver_dict
  return free_driver

def reloadPage(driver):
  driver.refresh();
  # skip bootloader
  try:
    skip = driver.find_element(By.XPATH, '//a[@class="skip-link" and text()="Skip"]')
    skip.click()
  except:
    # if app was installed  on a previous run, there is no bootloader page. contine
    pass
  # wait for editor iframe content
  driver.implicitly_wait(20)
  iframe = driver.find_element(By.XPATH, '//iframe')
  driver.implicitly_wait(0)

def runDriver(driver, combination):
  # fill drone inputs
  print("Running combination " + str(combination))
  reloadPage(driver)
  print("page reloaded!")
  for i, input_id in enumerate(DRONE_INPUT_ID_LIST):
    input = driver.find_element(By.ID, input_id)
    input.clear()
    input.send_keys(str(combination[i]))
  #run the simulation
  run_button = driver.find_element(By.XPATH, '//input[@type="submit" and @name="action_run"]')
  run_button.click()

##### MAIN #####

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
# TODO. HARDCODED, it should be generated by requesting the instances //see: script-slapos-request.py
server_url_list = [
  #"https://selenium:i1Kzu0Yd8L2R@[2001:67c:1254:53:b362::314f]:9430/wd/hub",
  "https://selenium:i1Kzu0Yd8L2R@softinst182376.host.vifib.net/wd/hub",
  #"https://selenium:dBlhn3DRcpgu@softinst182375.host.vifib.net/wd/hub"
]

for i in range(len(DRONE_VALUE_RANGE_LIST)):
  DRONE_INPUT_VALUE_LIST.append(values_in_range(DRONE_VALUE_RANGE_LIST[i][0], DRONE_VALUE_RANGE_LIST[i][1], GRANULARITY))

combination_list = [combination for combination in itertools.product(*DRONE_INPUT_VALUE_LIST)]

start_time = datetime.now()
print("Start execution at:")
print(start_time.strftime("%d/%m/%Y %H:%M:%S"))
print("Full combination_list:")
print(combination_list)

# configure the web driver settings
options = Options()
options.add_argument('headless')
options.add_argument('--headless=new')
options.add_argument('incognito')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')        
dc = DesiredCapabilities.CHROME
dc['loggingPrefs'] = { 'browser':'ALL'}

driver_list = []
for idx, server_url in enumerate(server_url_list):
  driver = setup_driver_on_app(server_url, options, dc)
  driver_dict = {
    'id': 'D' + str(idx),
    'server_url': server_url,
    'driver': driver,
    'first_run': True,
    'running_combination': None,
    'print-exception': False
  }
  driver_list.append(driver_dict)

iter = 0
while len(combination_list) > 0:
  print("---------------------------------")
  print("Combinations left: " + str(len(combination_list)))
  combination = combination_list.pop()
  iter += 1
  print("Allocating combination " + str(combination))
  assigned = False
  while not assigned:
    # check drivers
    # TODO: this may crash, include it in the try block
    driver_dict = getFreeDriver(combination)
    if driver_dict:
      print("Got free driver: " + str(driver_dict['id']))
      assigned = True
      print("Combination assigned to free driver")
      try:
        runDriver(driver_dict['driver'], combination)
      except Exception as e:
        print("ERROR: simulation for this combination failed")
        print(e)
        assigned = False
        print("trying to take screenshot...")
        try:
          takeFullScreenshot(driver_dict['driver'], '[ERROR] ' + str(combination) + '.png')
          #driver_dict['driver'].get_screenshot_as_file(str(combination) + '.png')
        except:
          print("Error while taking screenshot, this means driver sesion died. Re-creating webdriver...")
          driver_dict['driver'] = setup_driver_on_app(driver_dict.server_url, options, dc)
          driver_dict['running_combination'] = None
    else:
      print("No free drivers yet.")
      print("")
      time.sleep(1) #wait

print("")
print("--------------------------------")
print("ALL combinations were assigned")
print("--------------------------------")
print("")
print("waiting for current execution to end")
#wait until all running combination are done
finished = False
while not finished:
  finished = True
  for driver_dict in driver_list:
    # as this is the last check, it can be waited. No need to loop too much
    driver_dict['driver'].implicitly_wait(10)
    driver_dict['print-exception'] = True
    checkDriver(driver_dict)
    if driver_dict['running_combination']:
      finished = False
  time.sleep(0.5)

end_time = datetime.now()
print("End execution at:")
print(end_time.now().strftime("%d/%m/%Y %H:%M:%S"))
elapsed_time = end_time - start_time
print("Total combinations: " + str(iter))
print("Total time %s seconds. " % str(elapsed_time.seconds))

DEBUG = False
if DEBUG:
  for driver_dict in driver_list:
    #print browser log entries
    print("Log for driver " + str(driver_dict['id']))
    for entry in driver_dict['driver'].get_log('browser'):
      print(entry)
    driver_dict['driver'].quit()

print("All drivers quit")