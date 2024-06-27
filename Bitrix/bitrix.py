from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Front_base.locators_front import BitrixLocators
from Front_base.browser_works import Browser
import time
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
import pytest


class Bitrix(Browser):

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
            time.sleep(1)

    @staticmethod
    def order_link(order_id):

        return BitrixLocators.ORDER_CARD_LINK + str(order_id)

    @staticmethod
    def order_edit_link(order_id):

        return BitrixLocators.ORDER_EDIT_LINK + str(order_id)

    def order_status_change(self, order_status):

        select_element = self.find_element(*BitrixLocators.STATUS_SELECTOR)
        select = Select(select_element)
        select.select_by_value(order_status)
        save_status_button = self.find_element(*BitrixLocators.SAVE_STATUS_BUTTON)
        self.browser.scroll_into_view(save_status_button)
        self.click(save_status_button)
        print(f"Статус товара изменен на {order_status}")

    @pytest.mark.flaky(reruns=2)
    def change_buyout_status_to_yes(self):

        # self.scroll_into_view(*BitrixLocators.CHANGE_ITEM_POPUP_B)
        # change_item_popup = WebDriverWait(self.driver, 10).until(
        #     EC.element_to_be_clickable(BitrixLocators.CHANGE_ITEM_POPUP_B))
        # self.driver.execute_script("arguments[0].click();", change_item_popup)
        # change_item_button = self.find_element(*BitrixLocators.CHANGE_ITEM_BUTTON)
        # change_item_button.click()
        def click_on_item_popup(locator):
            try:
                self.scroll_into_view(*locator)
                WebDriverWait(self.browser, 10).until(EC.element_to_be_clickable(locator))
                self.click(self.find_element(*locator))
                change_item_button = self.find_element(*BitrixLocators.CHANGE_ITEM_BUTTON)
                self.click(change_item_button)
            except Exception as e:
                print(f"Не вышло кликнуть на попап товара. Пробуем снова")

        change_item_popup_a = BitrixLocators.CHANGE_ITEM_POPUP
        change_item_popup_b = BitrixLocators.CHANGE_ITEM_POPUP_B

        click_on_item_popup(change_item_popup_a)
        click_on_item_popup(change_item_popup_b)

        def enter_text_in_element(locator):
            try:
                self.scroll_into_view(*locator)
                self.find_element(*locator).clear()
                self.find_element(*locator).send_keys("Да")
            except Exception as e:
                print(f"Не вышло. Ошибка: {e}")

        purchased_inp_a = BitrixLocators.PURCHASED_INPUT_A
        purchased_inp_b = BitrixLocators.PURCHASED_INPUT_B

        enter_text_in_element(purchased_inp_a)
        enter_text_in_element(purchased_inp_b)

        change_item_save_button = self.find_element(*BitrixLocators.CHANGE_ITEM_SAVE_BUTTON)
        self.click(change_item_save_button)
        self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        save_order_changes_button = self.find_element(*BitrixLocators.SAVE_ORDER_CHANGES_BUTTON)
        self.browser.execute_script("arguments[0].click();", save_order_changes_button)
        print('Товар выкуплен')

    def change_pay_status_to_yes(self):
        change_pay_popup = self.find_element(*BitrixLocators.CHANGE_PAY_POPUP)
        self.browser.scroll_into_view(change_pay_popup)
        self.click(change_pay_popup)
        change_pay_to_yes_button = self.find_element(*BitrixLocators.CHANGE_PAY_TO_YES_BUTTON)
        self.browser.execute_script("arguments[0].click();", change_pay_to_yes_button)
        save_button = self.find_element(*BitrixLocators.CHANGE_PAY_SAVE_BUTTON)
        self.click(save_button)
