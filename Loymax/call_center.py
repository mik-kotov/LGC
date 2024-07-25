from Front_base.locators_front import LoyalLocators
from Loymax.base_page import LoymaxBasePage
from API import data
import time


class CallCenterPage(LoymaxBasePage):

    def go_to_search(self):
        self.go_to_call_center_page_from_main_page()
        search_frame = self.find_element(*LoyalLocators.SEARCH_USER_FRAME)
        self.browser.switch_to.frame(search_frame)
        search_button = self.find_element(*LoyalLocators.SEARCH_USER_BUTTON)
        self.click(search_button)

    def search_user(self, user_phone):
        phone_input = self.find_element(*LoyalLocators.SEARCH_USER_PHONE_INPUT)
        phone_input.send_keys(user_phone[1:])
        search_by_phone_button = self.find_element(*LoyalLocators.SEARCH_USER_BY_PHONE_BUTTON)
        self.click(search_by_phone_button)
        time.sleep(2)

