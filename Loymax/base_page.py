import time
import pytest
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Front_base.browser_works import browser
from Front_base.locators_front import BasePageLocators

class BasePage:
    def __init__(self, url="https://lgcity-stg.loymax.tech/#/", timeout=10):
        self.url = url
        self.browser = browser
        self.browser.implicitly_wait(timeout)

    def open(self, new_url):
        self.browser.get(new_url)

    def is_element_present(self, how, what):
        try:
            self.browser.find_element(how, what)
        except NoSuchElementException:
            return False
        return True

    def find_element(self, how, what):
        return self.browser.find_element(how, what)

    def is_not_element_present(self, how, what, timeout=4):
        try:
            WebDriverWait(self.browser, timeout).until(EC.presence_of_element_located((how, what)))
        except TimeoutException:
            return True

        return False

    def is_disappeared(self, how, what, timeout=4):
        try:
            WebDriverWait(self.browser, timeout, 1, TimeoutException).until_not(EC.presence_of_element_located((how, what)))
        except TimeoutException:
            return False

        return True

    def go_to_call_center_page(self):
        self.url = "https://lgcity-stg.loymax.tech/#/lmx/callcenter"
        self.open(self.url)

    def go_to_login_page(self):
        self.url = "https://lgcity-stg.loymax.tech/#/login"
        self.open(self.url)






