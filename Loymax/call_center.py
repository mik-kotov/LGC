from Front_base.locators_front import LoymaxLocators
from Loymax.base_page import BasePage
from Loymax.login_page import LoginPage
import time


class CallCenterPage(BasePage):

    def go_to_search(self):
        login_page = LoginPage()
        login_page.authorization()
        self.go_to_call_center_page()
        time.sleep(3)
        search_frame = self.find_element(*LoymaxLocators.SEARCH_USER_FRAME)
        time.sleep(3)
        self.browser.switch_to.frame(search_frame)
        time.sleep(3)
        search_button = self.find_element(*LoymaxLocators.SEARCH_USER_BUTTON)
        search_button.click()
        time.sleep(3)

    def search_user(self, user_phone):
        self.go_to_search()
        phone_input = self.find_element(*LoymaxLocators.SEARCH_USER_PHONE_INPUT)
        phone_input.send_keys(user_phone)
        search_by_phone_button = self.find_element(*LoymaxLocators.SEARCH_USER_BY_PHONE_BUTTON)
        search_by_phone_button.click()
        time.sleep(3)

