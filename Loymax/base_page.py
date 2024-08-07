from Front_base.browser_works import Browser
from Front_base.locators_front import LoyalLocators
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


class LoymaxBasePage(Browser):

    def go_to_deposit_page(self):
        self.open("https://lgcity-pstg.loymax.tech/#/home")
        self.wait_for_url("https://lgcity-pstg.loymax.tech/#/home")
        self.open("https://lgcity-pstg.loymax.tech/#/deposit/create")

    def go_to_home_page(self):
        self.open("https://lgcity-pstg.loymax.tech/#/home")

    def go_to_call_center_page_from_main_page(self):
        self.open("https://lgcity-pstg.loymax.tech/#/home")
        self.wait_for_url("https://lgcity-pstg.loymax.tech/#/home")
        self.open('https://lgcity-pstg.loymax.tech/#/lmx/callcenter')

    def go_to_login_page(self):
        self.open("https://lgcity-pstg.loymax.tech/#/login")




