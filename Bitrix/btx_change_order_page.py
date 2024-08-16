import time
from bitrix.btx_base_page import BitrixBasePage
from front_base.locators_front import BitrixLocators


class BitrixChangeOrderPage(BitrixBasePage):

    def go_to_order_page(self):
        button = self.find_element(*BitrixLocators.GO_TO_ORDER_FROM_CHANGE_ORDER_PAGE_BUTTON)
        self.scroll_into_view(button)
        button.click()
        time.sleep(3)

    def change_buyout_status_to_yes(self):
        popup = self.find_element(*BitrixLocators.CHANGE_ITEM_POPUP)
        self.scroll_to_element_centered(popup)
        self.click_js(popup)
        change_item_button = self.find_element(*BitrixLocators.CHANGE_ITEM_BUTTON)
        self.click_js(change_item_button)
        field = self.find_element(*BitrixLocators.PURCHASED_INPUT)
        self.scroll_into_view(field)
        field.clear()
        field.send_keys("Да")
        change_item_save_button = self.find_element(*BitrixLocators.CHANGE_ITEM_SAVE_BUTTON)
        self.click_js(change_item_save_button)
        self.scroll_to_bottom()
        save_order_changes_button = self.find_element(*BitrixLocators.SAVE_ORDER_CHANGES_BUTTON)
        self.click_js(save_order_changes_button)
        print('Товар выкуплен')

    def change_pay_status_to_yes(self):
        change_pay_popup = self.find_element(*BitrixLocators.CHANGE_PAY_POPUP)
        self.scroll_into_view(change_pay_popup)
        self.click(change_pay_popup)
        change_pay_to_yes_button = self.find_element(*BitrixLocators.CHANGE_PAY_TO_YES_BUTTON)
        self.browser.execute_script("arguments[0].click();", change_pay_to_yes_button)
        save_button = self.find_element(*BitrixLocators.CHANGE_PAY_SAVE_BUTTON)
        self.click(save_button)



