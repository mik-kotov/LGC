import time
import pytest
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Front_base.browser_works import Browser
from Front_base.locators_front import BasePageLocators

class LoymaxBasePage(Browser):

    def go_to_call_center_page(self):
        link = "https://lgcity-pstg.loymax.tech/#/lmx/callcenter"
        self.open(link)

    def go_to_login_page(self):
        link = "https://lgcity-pstg.loymax.tech/#/login"
        self.open(link)





