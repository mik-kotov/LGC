from API.data import loymax_password, loymax_login
from Front_base.locators_front import LoymaxLocators
from Loymax.base_page import BasePage
import time

class LoginPage(BasePage):
    url = "https://lgcity-stg.loymax.tech/#/login"
    def authorization(self):
        self.go_to_login_page()
        login_input = self.find_element(*LoymaxLocators.LOGIN_INPUT)
        login_input.send_keys(loymax_login)
        password_input = self.find_element(*LoymaxLocators.PASSWORD_INPUT)
        password_input.send_keys(loymax_password)
        authorization_button = self.find_element(*LoymaxLocators.AUTHORIZATION_BUTTON)
        authorization_button.click()
        time.sleep(10)









