from Front_base.locators_front import LoyalLocators
from Loymax.base_page import LoymaxBasePage
from Loymax.call_center import CallCenterPage
import time


class UserPage(LoymaxBasePage):

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
        assert f'<span class="b-table--responsive__value">{order_id}</span>' == str(order_number_html)
        print("Заказ есть в истории")

    def confirmation_check(self):
        assert self.is_element_present(*LoyalLocators.USER_PURCHASES_STATUS_CONFIRMED)
        print("Галка на месте")

    def cancellation_check(self):
        assert self.is_element_present(*LoyalLocators.USER_PURCHASES_STATUS_CANCELLED)
        print("Крестик на месте")

    def open_loupe(self):
        loupe_button = self.find_element(*LoyalLocators.USER_PURCHASE_LOUPE)
        loupe_button.click()

    def check_text_bonus(self):
        self.browser.execute_script("window.scrollBy(0, 500);")
        assert self.is_element_present(*LoyalLocators.TEXT_BONUS)

    def partial_cancel_two_statuses_check(self):
        self.browser.execute_script("window.scrollBy(0, 500);")
        assert ((self.find_element(*LoyalLocators.FIRST_FROM_TOP_PURCHASE_NUMBER).text) ==
                (self.find_element(*LoyalLocators.SECOND_FROM_TOP_PURCHASE_NUMBER).text))

    def partial_cancel_cancellation_check(self):
        assert self.is_element_present(*LoyalLocators.SECOND_FROM_TOP_PURCHASE_CANCELLED)

    def check_bonus_confirm(self):
        assert self.is_element_present(*LoyalLocators.BONUS_CONFIRMED)

    def check_added_bonuses_count_larger_than_null(self):

        bonus_rec = self.find_element(*LoyalLocators.ADDED_BONUSES_COUNT)
        text = bonus_rec.get_attribute('innerText').strip()
        count = float(text.replace('бнс.', '').strip())
        assert count > 0

    def check_paid_bonuses_count_less_than_null(self):
        bonus_rec = self.find_element(*LoyalLocators.PAID_BONUSES_COUNT)
        text = bonus_rec.get_attribute('innerText').strip()
        count = float(text.replace('бнс.', '').strip())
        assert count < 0
