from bitrix.btx_base_page import BitrixBasePage
from selenium.webdriver.common.by import By


class BitrixOrdersListPage(BitrixBasePage):

    def go_to_order_page(self):
        number_of_order_button = self.find_element(By.XPATH, f"//a[text()='№{self.order.order_number}']")
        number_of_order_button.click()

