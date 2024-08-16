from bitrix.btx_base_page import BitrixBasePage
from front_base.locators_front import BitrixLocators


class BitrixLoginPage(BitrixBasePage):

    def authorization(self):
        self.open(BitrixLocators.AUTHORIZATION_PAGE)
        if self.is_element_present(*BitrixLocators.AUTHORIZATION_WINDOW):
            login_input_field = self.find_element(*BitrixLocators.LOGIN_FIELD)
            password_input_field = self.find_element(*BitrixLocators.PASSWORD_FIELD)
            confirm_button = self.find_element(*BitrixLocators.CONFIRM_BUTTON)
            login_input_field.clear()
            login_input_field.send_keys(BitrixLocators.LOGIN)
            password_input_field.send_keys(BitrixLocators.PASSWORD)
            self.click(confirm_button)