from selenium.webdriver.chrome.service import Service
from selenium import webdriver


chrome_driver_path = r'C:\chromedriver\chromedriver.exe'
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("--headless")
service = Service(chrome_driver_path)
browser = webdriver.Chrome(service=service, options=options)

def start_work(browser, link):
    browser.get(link)

    return post_bonuses