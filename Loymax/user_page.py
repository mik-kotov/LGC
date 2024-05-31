from Front_base.locators_front import LoyalLocators
from Loymax.base_page import BasePage
from Loymax.call_center import CallCenterPage
import time


class UserPage(BasePage):

    def open_purchase_history(self):
        user_info_button = self.find_element(*LoyalLocators.USER_PERSONAL_INFO_BUTTON)
        user_info_button.click()
        user_purchases_button = self.find_element(*LoyalLocators.USER_PURCHASES_BUTTON)
        user_purchases_button.click()
        self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight)")

    def order_number_is_instance(self, order_id):
        order_number = self.find_element(*LoyalLocators.USER_PURCHASES_ORDER_NUMBER)
        order_number_html = order_number.get_attribute("outerHTML")
        time.sleep(1)
        assert f"<td>{order_id}</td>" == str(order_number_html)
        print("Заказ есть в истории")

    def confirmation_check(self):
        self.is_element_present(*LoyalLocators.USER_PURCHASES_STATUS_CONFIRMED)
        print("Галка на месте")
 return post_bonuses
