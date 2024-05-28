from Front_base.locators_front import LoymaxLocators
from Loymax.base_page import BasePage
from Loymax.call_center import CallCenterPage
import time


class UserPage(BasePage):

    def open_purchase_history(self):
        cc_page = CallCenterPage()
        cc_page.search_user(9160709800)
        user_info_button = self.find_element(*LoymaxLocators.USER_PERSONAL_INFO_BUTTON)
        user_info_button.click()
        user_purchases_button = self.find_element(*LoymaxLocators.USER_PURCHASES_BUTTON)
        user_purchases_button.click()
        self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight)")

    def order_number_is_instance(self):
        order_num = "1176611"
        order_number = self.find_element(*LoymaxLocators.USER_PURCHASES_ORDER_NUMBER)
        print(str(order_number.text))
        order_number.get_attribute("outerHTML")
        time.sleep(1)
        assert order_num == str(order_number.text)
        print("Заказ есть в истории")
    def confirmation_check(self):
        self.is_element_present(*LoymaxLocators.USER_PURCHASES_STATUS_CONFIRMED)
        print("Галка на месте")


up_test = UserPage()

for i in range(10):
    up_test.open_purchase_history()
    up_test.order_number_is_instance()
    up_test.confirmation_check()
