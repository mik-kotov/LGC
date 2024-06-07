from API.data import loymax_password, loymax_login
from Front_base.locators_front import LoyalLocators
from Loymax.base_page import BasePage
import time


class LoginPage(BasePage):

    def authorization(self):

        self.go_to_login_page()
        login_input = self.find_element(*LoyalLocators.LOGIN_INPUT)
        login_input.send_keys(loymax_login)
        password_input = self.find_element(*LoyalLocators.PASSWORD_INPUT)
        password_input.send_keys(loymax_password)
        authorization_button = self.find_element(*LoyalLocators.AUTHORIZATION_BUTTON)
        authorization_button.click()
        time.sleep(10)










