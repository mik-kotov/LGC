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
        save_status_button.click()
        print(f"Статус товара изменен на {order_status}")

    def change_buyout_status_to_yes(self):

        change_item_popup_logo = self.find_element(*BitrixLocators.CHANGE_ITEM_POPUP_LOGO)
        self.browser.execute_script("arguments[0].scrollIntoView(true);", change_item_popup_logo)
        change_item_popup = WebDriverWait(self.browser, 10).until(EC.element_to_be_clickable(BitrixLocators.CHANGE_ITEM_POPUP))
        self.browser.execute_script("arguments[0].click();", change_item_popup)
        change_item_button = self.find_element(*BitrixLocators.CHANGE_ITEM_BUTTON)
        change_item_button.click()
        self.find_element(By.XPATH,
                             "//div[@id='bx-admin-prefix']//input[@value='Выкуплен']/../self::td/following-sibling::td/input[@value='Нет']").clear()
        self.find_element(By.XPATH,
                             "//div[@id='bx-admin-prefix']//input[@value='Выкуплен']/../self::td/following-sibling::td/input[@value='Нет']").send_keys("Да")
        change_item_save_button = self.find_element(*BitrixLocators.CHANGE_ITEM_SAVE_BUTTON)
        change_item_save_button.click()
        save_order_changes_button = self.find_element(*BitrixLocators.SAVE_ORDER_CHANGES_BUTTON)
        save_order_changes_button.click()
        print('Товар выкуплен')


# b = Bitrix()
# b.authorization()
# time.sleep(2)
# b.open(Bitrix.order_edit_link(1176796))
# b.change_buyout_status_to_yes()
# time.sleep(2)

