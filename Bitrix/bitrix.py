from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from Front_base.locators_front import BitrixLocators
from Front_base.browser_works import Browser
import time
from selenium.webdriver.support.ui import Select
from Front_base.browser_works import retry


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

    def order_link(self):

        return BitrixLocators.ORDER_CARD_LINK + str(self.order.order_number)

    def order_edit_link(self):

        return BitrixLocators.ORDER_EDIT_LINK + str(self.order.order_number)

    def order_status_change(self, order_status):

        select_element = self.find_element(*BitrixLocators.STATUS_SELECTOR)
        select = Select(select_element)
        select.select_by_value(order_status)
        save_status_button = self.find_element(*BitrixLocators.SAVE_STATUS_BUTTON)
        self.scroll_into_view(save_status_button)
        self.click(save_status_button)
        print(f"Статус товара изменен на {order_status}")

    def change_buyout_status_to_yes(self):


        if not self.is_element_present(*BitrixLocators.GO_TO_ORDER_FROM_CHANGE_ORDER_PAGE_BUTTON):
            print("Переоткрываем страницу 'Изменить заказ'")
            self.open(self.order_link())
            self.open(self.order_edit_link())
        button = self.find_element(By.XPATH,
                                         '//div[@class=\"adm-bus-component-title\" and text()=\"Заказ\"]/ancestor::div[@id="tab_order"]/div/table/tbody/tr/td/div/div[7]//div[@class="adm-bus-statusorder"]//table/tbody[3]//span[@class="adm-s-order-item-title-icon"]')
        self.scroll_into_view(button)
        WebDriverWait(self.browser, 10).until(EC.element_to_be_clickable(button))
        self.browser.execute_script("arguments[0].click();", button)
        CHANGE_ITEM_BUTTON = self.find_element(By.CSS_SELECTOR,
                                                     ".bx-core-popup-menu-item-default .bx-core-popup-menu-item-text")
        self.browser.execute_script("arguments[0].click();", CHANGE_ITEM_BUTTON)

        element = self.find_element(*BitrixLocators.PURCHASED_INPUT_A)
        self.scroll_into_view(element)
        element.clear()
        element.send_keys("Да")

        change_item_save_button = self.find_element(*BitrixLocators.CHANGE_ITEM_SAVE_BUTTON)
        self.browser.execute_script("arguments[0].click();", change_item_save_button)
        self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        save_order_changes_button = self.find_element(*BitrixLocators.SAVE_ORDER_CHANGES_BUTTON)
        self.browser.execute_script("arguments[0].click();", save_order_changes_button)
        print('Товар выкуплен')

    def change_pay_status_to_yes(self):
        change_pay_popup = self.find_element(*BitrixLocators.CHANGE_PAY_POPUP)
        self.scroll_into_view(change_pay_popup)
        self.click(change_pay_popup)
        change_pay_to_yes_button = self.find_element(*BitrixLocators.CHANGE_PAY_TO_YES_BUTTON)
        self.browser.execute_script("arguments[0].click();", change_pay_to_yes_button)
        save_button = self.find_element(*BitrixLocators.CHANGE_PAY_SAVE_BUTTON)
        self.click(save_button)

        self.click(save_button)

    def check_promocode_exists(self):
        assert self.is_element_present(*BitrixLocators.PROMOCODE_FIELD)
        assert self.is_element_present(*BitrixLocators.PROMOCODE_NAME)
        promocode_name = self.browser.find_element(*BitrixLocators.PROMOCODE_NAME)
        name = promocode_name.get_attribute('innerText').strip()
        assert name == self.order.promocode_name

    def check_order_sum_with_promo(self):
        order_price = self.find_element(*BitrixLocators.FINAL_PRICE_WITHOUT_BONUSES)
        price = int(order_price.get_attribute('innerText').replace(" ", ""))
        print(price)
        print(self.order.price_final)
        assert self.order.price_final + self.order.bonuses == price
