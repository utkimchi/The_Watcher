import time
import os
from os.path import join, dirname
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv


################################
#MAIN
################################


dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
lb_user = os.getenv("LB_USERNAME")
lb_pass = os.getenv("LB_PASSWORD")

adblock_path = join(dirname(__file__), 'AdBlock')


options = Options()
#options.add_argument('--headless=new')
options.add_argument('load-extension=' + adblock_path)
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')

driver = webdriver.Chrome(options=options)
driver.implicitly_wait(5)
actions = ActionChains(driver)
driver.get('https://letterboxd.com/sign-in/')

element = WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.XPATH, "//input[@name='username']")))
element = driver.find_element(By.XPATH, "//input[@name='username']")
element.send_keys(lb_user)
element = driver.find_element(By.XPATH, "//input[@name='password']")
element.send_keys(lb_pass)
element.submit()

try:
    element = WebDriverWait(driver, 2).until(EC.staleness_of(driver.find_element(By.XPATH, "//input[@name='username']")))
except:
    print("?")

# try: 
#     element = WebDriverWait(driver, 5).until(EC.visibility_of((By.XPATH, "//a[contains(.,{lb_user})]")))
# except: 
#     print("Loading took too much time!") 

movie_title = "https://letterboxd.com/film/the-lighthouse-2019/"
driver.get(movie_title)

element = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.LINK_TEXT, "Add to lists…")))
element.click()
element = driver.find_element(By.XPATH, '//span[contains(.,"Kinosphere")]')
element.click()
element.submit()

driver.get("https://letterboxd.com/beeferweller/list/kinosphere/")

time.sleep(5) # Let the user actually see something!



driver.quit()