from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
import pytest
from selenium.webdriver import Remote as RemoteWebDriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import allure
from selenium.webdriver.common.by import By
from Front_base import locators_front
import time

# chrome_driver_path = r'C:\chromedriver\chromedriver.exe'
# options = webdriver.ChromeOptions()
# options.add_argument("--start-maximized")
# #options.add_argument("--headless")
# service = Service(chrome_driver_path)
# driver = webdriver.Chrome(service=service, options=options)
# driver.implicitly_wait(10)

class Browser:

    def __init__(self, browser):

        self.browser = browser
        self.browser.implicitly_wait(10)

    def open(self, link):

        self.browser.get(link)

    def click(self, locator):

        locator.click()
        allure.attach(self.browser.get_screenshot_as_png(),
                      name='Click_Screenshot', attachment_type=allure.attachment_type.PNG)

    def find_element(self, how, what, timeout=10):

        element = WebDriverWait(self.browser, timeout).until(
            EC.presence_of_element_located((how, what))
        )
        return element


    def find_elements(self, how, what):

        return self.browser.find_elements(how, what)

    def scroll_into_view(self, how, what):

        return self.browser.execute_script('arguments[0].scrollIntoView({block: "center"});',
                                           self.browser.find_element(how, what))

    def is_element_present(self, how, what):
        try:
            self.browser.find_element(how, what)
        except NoSuchElementException:
            return False
        return True

    def is_not_element_present(self, how, what, timeout=4):
        try:
            WebDriverWait(self.browser, timeout).until(EC.presence_of_element_located((how, what)))
        except TimeoutException:
            return True

        return False
