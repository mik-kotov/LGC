from API.data import loymax_password, loymax_login
from Front_base.locators_front import LoyalLocators
from Loymax.base_page import LoymaxBasePage


class LoymaxLoginPage(LoymaxBasePage):

    def authorization(self):

        link = "https://lgcity-pstg.loymax.tech/#/login"
        self.open(link)
        if self.is_element_present(*LoyalLocators.LOGIN_INPUT):
            self.go_to_login_page()
            login_input = self.find_element(*LoyalLocators.LOGIN_INPUT)
            login_input.send_keys(loymax_login)
            password_input = self.find_element(*LoyalLocators.PASSWORD_INPUT)
            password_input.send_keys(loymax_password)
            authorization_button = self.find_element(*LoyalLocators.AUTHORIZATION_BUTTON)
            self.click(authorization_button)










