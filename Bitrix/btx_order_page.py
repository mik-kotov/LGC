from bitrix.btx_base_page import BitrixBasePage
from front_base.locators_front import BitrixLocators
from selenium.webdriver.support.ui import Select


class BitrixOrderPage(BitrixBasePage):

    def go_to_change_order_page(self):
        button = self.find_element(*BitrixLocators.GO_TO_CHANGE_ORDER_PAGE_FROM_ORDER_BUTTON)
        self.scroll_into_view(button)
        button.click()

    def order_status_change(self, order_status):
        select_element = self.find_element(*BitrixLocators.STATUS_SELECTOR)
        select = Select(select_element)
        select.select_by_value(order_status)
        save_status_button = self.find_element(*BitrixLocators.SAVE_STATUS_BUTTON)
        self.scroll_into_view(save_status_button)
        self.click(save_status_button)
        print(f"Статус товара изменен на {order_status}")

    def check_promocode_exists(self):
        self.scroll_to_bottom()
        assert self.is_element_present(*BitrixLocators.PROMOCODE_FIELD)
        assert self.is_element_present(*BitrixLocators.PROMOCODE_NAME)
        promocode_name = self.browser.find_element(*BitrixLocators.PROMOCODE_NAME)
        name = promocode_name.get_attribute('innerText').strip()
        assert name == self.order.promocode_name

    def check_order_sum_with_promo(self):
        self.scroll_to_bottom()
        order_price = self.find_element(*BitrixLocators.FINAL_PRICE_WITHOUT_BONUSES)
        price = int(order_price.get_attribute('innerText').replace(" ", ""))
        assert self.order.price_final + self.order.bonuses == price