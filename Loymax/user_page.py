from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Front_base.locators_front import LoyalLocators
from Loymax.base_page import LoymaxBasePage
import re

import time
import allure


class UserPage(LoymaxBasePage):


    def open_purchase_history(self):
        user_info_button = self.find_element(*LoyalLocators.USER_PERSONAL_INFO_BUTTON)
        self.click(user_info_button)
        user_purchases_button = self.find_element(*LoyalLocators.USER_PURCHASES_BUTTON)
        self.click(user_purchases_button)

    def get_history_screenshot(self):
        purchases_table = self.find_element(*LoyalLocators.USER_PURCHASES_TABLE)
        WebDriverWait(self.browser, 10).until(EC.visibility_of_element_located(LoyalLocators.USER_PURCHASES_TABLE))
        self.scroll_into_view(purchases_table)
        allure.attach(self.browser.get_screenshot_as_png(), name="Скриншот истории заказов",
                      attachment_type=allure.attachment_type.PNG)

    def order_number_is_instance(self):
        self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        order_number = self.find_element(*LoyalLocators.USER_PURCHASES_ORDER_NUMBER)
        order_number_txt = order_number.get_attribute('innerText')
        print(str(order_number_txt))
        assert str(self.order.order_number) == str(order_number_txt)
        print("Заказ есть в истории")

    def confirmation_check(self):
        assert self.is_element_present(*LoyalLocators.USER_PURCHASES_STATUS_CONFIRMED)
        print("Галка на месте")

    def cancellation_check(self):
        assert self.is_element_present(*LoyalLocators.USER_PURCHASES_STATUS_CANCELLED)
        print("Крестик на месте")

    def creation_check(self):
        assert self.is_element_present(*LoyalLocators.USER_PURCHASES_STATUS_CREATED)

    def open_loupe(self):
        loupe_button = self.find_element(*LoyalLocators.USER_PURCHASE_LOUPE)
        self.click(loupe_button)
        time.sleep(10)
        self.browser.execute_script("window.scrollBy(0, 1700);")

    def second_purchase_open_loup(self):
        loupe_button = self.find_element(*LoyalLocators.SECOND_FROM_TOP_PURCHASE_LOUPE)
        self.click(loupe_button)
        self.browser.execute_script("window.scrollBy(0, 1700);")

    def check_text_bonus(self):
        assert self.is_element_present(*LoyalLocators.TEXT_ADDED_BONUS)

    def from_purchase_back_to_history(self):
        button = self.find_element(*LoyalLocators.BUTTON_BACK_TO_HISTORY)
        self.click(button)

    def partial_cancel_two_statuses_check(self):
        self.browser.execute_script("window.scrollBy(0, 500);")
        assert (self.find_element(*LoyalLocators.FIRST_FROM_TOP_PURCHASE_NUMBER).text ==
                self.find_element(*LoyalLocators.SECOND_FROM_TOP_PURCHASE_NUMBER).text)

    def partial_cancel_cancellation_check(self):
        assert self.is_element_present(*LoyalLocators.SECOND_FROM_TOP_PURCHASE_CANCELLED)

    def check_added_bonus_confirm(self):
        assert self.is_element_present(*LoyalLocators.ADDED_BONUS_CONFIRMED)

    def check_added_bonus_cancelled(self):
        assert self.is_element_present(*LoyalLocators.ADDED_BONUS_CANCELLED)

    def check_added_bonuses_count_larger_than_null(self):
        bonus_rec = self.find_element(*LoyalLocators.ADDED_BONUSES_COUNT)
        text = bonus_rec.get_attribute('innerText').strip()
        count = float(text.replace('бнс.', '').strip())
        assert count > 0

    def check_paid_bonus_confirmed(self):
        assert self.is_element_present(*LoyalLocators.PAID_BONUS_CONFIRMED)

    def check_paid_bonus_cancelled(self):
        assert self.is_element_present(*LoyalLocators.PAID_BONUS_CANCELLED)

    def check_paid_bonuses_count_less_than_null(self):
        bonus_rec = self.find_element(*LoyalLocators.PAID_BONUSES_COUNT)
        text = bonus_rec.get_attribute('innerText').strip()
        count = float(text.replace('бнс.', '').strip())
        assert count < 0

    def check_used_promocode_is_exist(self):
        promo_text = self.find_element(*LoyalLocators.USED_PROMOCODE)
        text = promo_text.get_attribute('innerText').strip()
        assert text == self.order.promocode_name.upper()

    def check_order_sum_with_promo(self):
        sum_text = self.find_element(*LoyalLocators.LOYMAX_ORDER_SUM)
        price = sum_text.get_attribute('innerText')[:-4]
        match = re.search(r'(\d[\d\s]*)', price)
        number_str = match.group(1)
        number_str = ''.join(number_str.split())
        print(number_str)
        print(self.order.price_final)
        assert str(self.order.price_final) == number_str

