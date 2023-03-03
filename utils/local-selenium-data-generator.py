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

start_time = datetime.now()
print("Start execution at:")
print(start_time.strftime("%d/%m/%Y %H:%M:%S"))

NUMBER_OF_DRONES = 1
GRANULARITY = 8
GAME_INPUT_ID_LIST=["simulation_speed", "simulation_time", "number_of_drones", "drone_min_speed", "drone_max_speed", "drone_max_acceleration", "drone_max_deceleration", "start_AMSL", "init_pos_lat", "init_pos_lon", "init_pos_z", "drone_max_sink_rate", "drone_max_climb_rate"]
GAME_INPUT_VALUE_LIST=[1500*60, 1500, NUMBER_OF_DRONES, 12, 20, 6, 1, "594.792", "45.6403", "14.2648", "65.668", 3, 8]
DRONE_INPUT_ID_LIST=["drone_speed", "drone_max_roll", "drone_min_pitch", "drone_max_pitch"]
DRONE_VALUE_RANGE_LIST=[[12.1, 19.9], [10, 50], [-35, -10], [10, 40]]
#DRONE_VALUE_RANGE_LIST=[[12, 52], [-37, -11], [12, 38]]
DRONE_INPUT_VALUE_LIST=[]
AI_SCRIPT = open("my_script.js", "r").read()

def values_in_range(start, end, n):
  d = (end - start) / (n - 1)
  return [start + i*d for i in range(n)]

for i in range(len(DRONE_VALUE_RANGE_LIST)):
  DRONE_INPUT_VALUE_LIST.append(values_in_range(DRONE_VALUE_RANGE_LIST[i][0], DRONE_VALUE_RANGE_LIST[i][1], GRANULARITY))

def setup_driver_on_app(options, dc):
  done = False
  retry = 0
  while not done:
    if retry == 10:
        raise RuntimeError("Error: couldn't create webdriver after 10 attempts")
    try:
        # local selenium
        driver = webdriver.Chrome(options=options, desired_capabilities=dc)

        # navigate to drone app
        url = "https://dronesimulator.app.officejs.com/"
        #url = "https://softinst157899.host.vifib.net/erp5/web_site_module/officejs_drone_simulator/"
        driver.get(url)
        driver.implicitly_wait(5)
        # skip bootloader
        try:
          skip = driver.find_element(By.XPATH, '//a[@class="skip-link" and text()="Skip"]')
          skip.click()
        except:
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
        frame = driver.find_element(By.XPATH, '//iframe')
        driver.switch_to.frame(frame)
        driver.execute_script('return document.getElementsByClassName("CodeMirror")[0].CodeMirror.setValue("' + AI_SCRIPT.replace("\n", "\\n") + '")')
        driver.switch_to.default_content()

        print("Webdriver created.")
        done = True
    except Exception as e:
        print("Error creating webdriver.")
        print(e)
        print("retry")
        retry += 1
  return driver

# configure the web driver settings
options = Options()
options.add_argument('headless')
options.add_argument('incognito')
options.add_argument('window-size=1200x1200')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')        
dc = DesiredCapabilities.CHROME
dc['loggingPrefs'] = { 'browser':'ALL'}

driver = setup_driver_on_app(options, dc)
iter = 0
# run all combination of input values
for combination in itertools.product(*DRONE_INPUT_VALUE_LIST):
  iter += 1
  try:
    # fill drone inputs
    print("Running combination " + str(combination))
    #print(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    start_iter = datetime.now()
    for i, input_id in enumerate(DRONE_INPUT_ID_LIST):
      input = driver.find_element(By.ID, input_id)
      input.clear()
      input.send_keys(str(combination[i]))
      #driver.get_screenshot_as_file(str(combination) + '.png')

    #'''
    #run the simulation
    run_button = driver.find_element(By.XPATH, '//input[@type="submit" and @name="action_run"]')
    run_button.click()

    driver.implicitly_wait(30)
    loading = driver.find_element(By.XPATH, '//span[@id="loading"]')
    driver.find_element(By.XPATH, '//div[@class="container"]//a[contains(text(), "Download Simulation LOG")]')

    # download all result logs
    for i in range(NUMBER_OF_DRONES):
      text = "Download Simulation LOG " + str(i)
      download_log = driver.find_element(By.XPATH, '//div[@class="container"]//a[contains(text(), "' + text + '")]')
      download_log.click() #saves log txt file in command location

    end_iter = datetime.now()
    elapsed = end_iter - start_iter
    print("* done in %s milliseconds: " % str(elapsed.total_seconds()*1000))
    #'''
  except Exception as e:
    print("ERROR: simulation for this combination failed")
    print(e)
    print("trying to take screenshot...")
    try:
      driver.get_screenshot_as_file(str(combination) + '.png')
    except:
      print("Error while taking screenshot, this means driver sesion ended. Re-creating webdriver...")
      driver = setup_driver_on_app(options, dc)

end_time = datetime.now()
print("End execution at:")
print(end_time.now().strftime("%d/%m/%Y %H:%M:%S"))
elapsed_time = end_time - start_time
print("Total combinations: " + str(iter))
print("Total time %s seconds. " % str(elapsed_time.seconds))

