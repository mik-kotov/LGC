from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Front_base.locators_front import BitrixLocators

from Front_base.browser_works import Browser
import time
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By


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
            confirm_button.click()
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
        self.browser.execute_script('arguments[0].scrollIntoView({block: "center"});',  save_status_button)
        save_status_button.click()
        print(f"Статус товара изменен на {order_status}")

    def change_buyout_status_to_yes(self):

        self.scroll_into_view(*BitrixLocators.CHANGE_ITEM_POPUP_LOGO)
        change_item_popup = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable(BitrixLocators.CHANGE_ITEM_POPUP))
        self.browser.execute_script("arguments[0].click();", change_item_popup)
        change_item_button = self.find_element(*BitrixLocators.CHANGE_ITEM_BUTTON)
        change_item_button.click()

        def enter_text_in_element(locator, text):
            try:
                self.scroll_into_view(*locator)
                self.find_element(*locator).clear()
                self.find_element(*locator).send_keys(text)
            except Exception as e:
                print(f"Не вышло. Пробуем план Б. Ошибка: {e}")

        # Использование функции для первого и второго случаев
        purchased_inp_a = BitrixLocators.PURCHASED_INPUT_A
        purchased_inp_b = BitrixLocators.PURCHASED_INPUT_B

        enter_text_in_element(purchased_inp_a, text="Да")
        enter_text_in_element(purchased_inp_b, text="Да")

        change_item_save_button = self.find_element(*BitrixLocators.CHANGE_ITEM_SAVE_BUTTON)
        change_item_save_button.click()
        self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        save_order_changes_button = self.find_element(*BitrixLocators.SAVE_ORDER_CHANGES_BUTTON)
        self.browser.execute_script("arguments[0].click();", save_order_changes_button)
        print('Товар выкуплен')

    def change_pay_status_to_yes(self):
        change_pay_popup = self.find_element(*BitrixLocators.CHANGE_PAY_POPUP)
        self.browser.execute_script('arguments[0].scrollIntoView({block: "center"});', change_pay_popup)
        change_pay_popup.click()
        change_pay_to_yes_button = self.find_element(*BitrixLocators.CHANGE_PAY_TO_YES_BUTTON)
        self.browser.execute_script("arguments[0].click();", change_pay_to_yes_button)
        save_button = self.find_element(*BitrixLocators.CHANGE_PAY_SAVE_BUTTON)
        save_button.click()
