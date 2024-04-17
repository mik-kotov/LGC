from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
import time


chrome_driver_path = r'C:\chromedriver\chromedriver.exe'
user_data_dir = r'C:\Users\QASQUAD\AppData\Local\Google\Chrome\User Data\Profile 4'
options = webdriver.ChromeOptions()
options.add_argument(f'--user-data-dir={user_data_dir}')
service = Service(chrome_driver_path)
browser = webdriver.Chrome(service=service, options=options)

def start_work(browser, link):
    browser.get(link)