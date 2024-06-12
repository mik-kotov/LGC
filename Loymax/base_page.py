import time
import pytest
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Front_base.browser_works import Browser
from Front_base.locators_front import LoyalLocators

class LoymaxBasePage(Browser):

    def go_to_call_center_page_from_main_page(self):
        call_center_button = self.find_element(*LoyalLocators.CONTACT_CENTER_BUTTON)
        call_center_button.click()

    def go_to_login_page(self):
        link = "https://lgcity-pstg.loymax.tech/#/login"
        self.open(link)





