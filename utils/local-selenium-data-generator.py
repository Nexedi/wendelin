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

print("Start execution at:")
print(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))

NUMBER_OF_DRONES = 1
GRANULARITY = 3
GAME_INPUT_ID_LIST=["simulation_speed", "simulation_time", "number_of_drones", "drone_min_speed", "drone_speed", "drone_max_speed", "drone_max_acceleration", "drone_max_deceleration"]
GAME_INPUT_VALUE_LIST=[300, 1500, NUMBER_OF_DRONES, 10, 15, 30, 6, 1]
DRONE_INPUT_ID_LIST=["drone_max_roll", "drone_min_pitch", "drone_max_pitch", "drone_max_sink_rate", "drone_max_climb_rate"]
DRONE_VALUE_RANGE_LIST=[[0, 90], [-50, 0], [0, 50], [-15, 30], [-1, 30]]
DRONE_INPUT_VALUE_LIST=[]

def values_in_range(start, end, n):
  d = (end - start) / (n - 1)
  return [start + i*d for i in range(n)]

for i in range(len(DRONE_VALUE_RANGE_LIST)):
  DRONE_INPUT_VALUE_LIST.append(values_in_range(DRONE_VALUE_RANGE_LIST[i][0], DRONE_VALUE_RANGE_LIST[i][1], GRANULARITY))

#speed  1 - 30 (min<sp<max)
#accel  1 - 10
#roll   0 - 90
#pitch -50 - 50 (min<max)
#sink  -15 - 30  (<max_speed)
#climb  -1 - 30  (<max_speed)

# configure the web driver settings
options = Options()
options.add_argument('headless')
options.add_argument('incognito')
options.add_argument('window-size=1200x2600')
dc = DesiredCapabilities.CHROME
dc['loggingPrefs'] = { 'browser':'ALL'}

# local selenium
driver = webdriver.Chrome(options=options, desired_capabilities=dc)

# navigate to drone app
url = "https://dronesimulator.app.officejs.com/"
url = "https://softinst157899.host.vifib.net/erp5/web_site_module/officejs_drone_simulator/"
driver.get(url)
driver.implicitly_wait(5)
# skip bootloader
skip = driver.find_element(By.XPATH, '//a[@class="skip-link" and text()="Skip"]')
skip.click()

# wait for editor iframe content
driver.implicitly_wait(10)
iframe = driver.find_element(By.XPATH, '//iframe')

# fill game inputs
for i, input_id in enumerate(GAME_INPUT_ID_LIST):
  input = driver.find_element(By.ID, input_id)
  input.clear()
  input.send_keys(GAME_INPUT_VALUE_LIST[i])

# run all combination of input values
for combination in itertools.product(*DRONE_INPUT_VALUE_LIST):
  # fill drone inputs
  print("* running combination " + str(combination))
  for i, input_id in enumerate(DRONE_INPUT_ID_LIST):
    input = driver.find_element(By.ID, input_id)
    input.clear()
    input.send_keys(int(combination[i]))

  #run the simulation
  run_button = driver.find_element(By.XPATH, '//input[@type="submit" and @name="action_run"]')
  run_button.click()

  driver.implicitly_wait(30)
  loading = driver.find_element(By.XPATH, '//span[@id="loading"]')
  time.sleep(20)

  # download all result logs
  for i in range(NUMBER_OF_DRONES):
    text = "Download Simulation LOG " + str(i)
    download_log = driver.find_element(By.XPATH, '//div[@class="container"]//a[contains(text(), "' + text + '")]')
    download_log.click() #saves log txt file in command location

print("End execution at:")
print(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
#screenshot
#driver.get_screenshot_as_file('main-page.png')

