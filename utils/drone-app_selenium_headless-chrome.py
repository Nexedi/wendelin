INPUT_ID_LIST=["simulation_speed", "simulation_time", "drone_speed"]
INPUT_VALUE_LIST=[300, 1000, 10]
NUMBER_OF_DRONES = 3

import certifi
import urllib3
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.remote.remote_connection import RemoteConnection

options = Options()
options.add_argument('headless')
options.add_argument('window-size=1200x2600')
d = DesiredCapabilities.CHROME
d['loggingPrefs'] = { 'browser':'ALL'}
driver = webdriver.Chrome(options=options, desired_capabilities=d)

print("declaring webdriver remote server")
server_url = "https://selenium:jvT0SRR9Mtad@[2001:67c:1254:5f:d58a::5933]:9443/wd/hub"
executor = RemoteConnection(server_url, keep_alive=True)
cert_reqs = 'CERT_REQUIRED'
ca_certs = certifi.where()
#if not test_runner.get('verify-server-certificate', True):
#  cert_reqs = 'CERT_NONE'
#  ca_certs = None
#if test_runner.get('server-ca-certificate'):
#  ca_certs = os.path.join(ETC_DIRECTORY, "cacerts.pem")
#  with open(ca_certs, 'w') as f:
#    f.write(test_runner.get('server-ca-certificate'))
executor._conn = urllib3.PoolManager(cert_reqs=cert_reqs, ca_certs=ca_certs)

browser = webdriver.Remote(
    command_executor=executor,
    desired_capabilities=d,
)

# if all ok, use 'browser' instead of local webdriver created on var 'driver'

url = "https://dronesimulator.app.officejs.com/"
driver.get(url)
driver.implicitly_wait(5)
skip = driver.find_element(By.XPATH, '//a[@class="skip-link" and text()="Skip"]')
skip.click()

#wait for editor iframe content
driver.implicitly_wait(10)
iframe = driver.find_element(By.XPATH, '//iframe')

for i, input_id in enumerate(INPUT_ID_LIST):
  input = driver.find_element(By.ID, input_id)
  input.clear()
  input.send_keys(INPUT_VALUE_LIST[i])

input = driver.find_element(By.ID, "number_of_drones")
input.clear()
input.send_keys(NUMBER_OF_DRONES)

# how to change iframe html content??
#frame = driver.find_element(By.XPATH, '//iframe')
#driver.switch_to.frame(frame)
#do stuff
#codemirror = driver.find_elements_by_class_name("CodeMirror-code")
#driver.switch_to.default_content()

run_button = driver.find_element(By.XPATH, '//input[@type="submit" and @name="action_run"]')
run_button.click()

loading = driver.find_element(By.XPATH, '//span[@id="loading"]')
driver.implicitly_wait(20)

for i in range(NUMBER_OF_DRONES):
  text = "Download Simulation LOG " + str(i)
  download_log = driver.find_element(By.XPATH, '//div[@class="container"]//a[contains(text(), "' + text + '")]')
  download_log.click() #saves log txt file in command location

# at this point, we have all the drone logs generated as txt files in command execution directory

#print browser log entries
for entry in driver.get_log('browser'):
  print(entry)

driver.quit()
