NUMBER_OF_DRONES = 1
INPUT_ID_LIST=["simulation_speed", "simulation_time", "drone_speed", "number_of_drones"]
INPUT_VALUE_LIST=[300, 1000, 10, NUMBER_OF_DRONES]
AI_SCRIPT = 'me.onStart = function () {console.log(111111);};'

import certifi
import urllib3
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.remote.remote_connection import RemoteConnection

# configure the web driver settings
options = Options()
options.add_argument('headless')
options.add_argument('window-size=1200x2600')
dc = DesiredCapabilities.CHROME
dc['loggingPrefs'] = { 'browser':'ALL'}

# local selenium
driver = webdriver.Chrome(options=options, desired_capabilities=dc)

# run selenium remote server
server_url = "https://selenium:jvT0SRR9Mtad@softinst179949.host.vifib.net/wd/hub"
executor = RemoteConnection(server_url, keep_alive=True)
cert_reqs = 'CERT_REQUIRED'
ca_certs = certifi.where()
executor._conn = urllib3.PoolManager(cert_reqs=cert_reqs, ca_certs=ca_certs)
driver = webdriver.Remote(
    command_executor=executor,
    desired_capabilities=dc,
)

# navigate to drone app
url = "https://dronesimulator.app.officejs.com/"
driver.get(url)
driver.implicitly_wait(5)
# skip bootloader
skip = driver.find_element(By.XPATH, '//a[@class="skip-link" and text()="Skip"]')
skip.click()

# wait for editor iframe content
driver.implicitly_wait(10)
iframe = driver.find_element(By.XPATH, '//iframe')

# fill all standard inputs
for i, input_id in enumerate(INPUT_ID_LIST):
  input = driver.find_element(By.ID, input_id)
  input.clear()
  input.send_keys(INPUT_VALUE_LIST[i])

# fill codemirror editor input
frame = driver.find_element(By.XPATH, '//iframe')
driver.switch_to.frame(frame)
driver.execute_script('return document.getElementsByClassName("CodeMirror")[0].CodeMirror.setValue("' + AI_SCRIPT + '")')
driver.switch_to.default_content()

#run the simulation
run_button = driver.find_element(By.XPATH, '//input[@type="submit" and @name="action_run"]')
run_button.click()

driver.implicitly_wait(30)
loading = driver.find_element(By.XPATH, '//span[@id="loading"]')

time.sleep(20)
#screenshot
driver.get_screenshot_as_file('main-page.png')

# download all result logs
for i in range(NUMBER_OF_DRONES):
  text = "Download Simulation LOG " + str(i)
  download_log = driver.find_element(By.XPATH, '//div[@class="container"]//a[contains(text(), "' + text + '")]')
  download_log.click() #saves log txt file in command location

# at this point, we have all the drone logs generated as txt files in command execution directory

#screenshot
driver.get_screenshot_as_file('main-page.png')

#print browser log entries
for entry in driver.get_log('browser'):
  print(entry)

driver.quit()
