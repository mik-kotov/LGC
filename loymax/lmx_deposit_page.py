from front_base.locators_front import LoyalLocators
from loymax.lmx_base_page import LoymaxBasePage
import allure


class DepositPage(LoymaxBasePage):

    def choose_accrual_option(self):
        accrual_button = self.find_element(*LoyalLocators.ACCRUAL_RADIOBUTTON)
        self.click(accrual_button)

    def select_company(self):
        select_list = self.find_element(*LoyalLocators.SELECT_COMPANY_LIST)
        self.click(select_list)
        option = self.find_element(*LoyalLocators.OOO_TRADE_MANAGEMENT)
        self.click(option)

    def select_currency(self):
        select_list = self.find_element(*LoyalLocators.CURRENCIES_LIST)
        self.click(select_list)
        option = self.find_element(*LoyalLocators.CHOOSE_BONUSES_AS_CURRENCY)
        self.click(option)

    def fill_description_field(self):
        field = self.find_element(*LoyalLocators.DESCRIPTION_FIELD)
        field.send_keys("Тест")

    def fill_internal_description_field(self):
        field = self.find_element(*LoyalLocators.INTERNAL_DESCRIPTION_FIELD)
        field.send_keys("Тест")

    def choose_manual_input_option(self):
        radiobutton = self.find_element(*LoyalLocators.MANUAL_INPUT_RADIOBUTTON)
        self.click(radiobutton)

    def select_id_in_list(self):
        select_list = self.find_element(*LoyalLocators.CHOOSE_ID)
        self.click(select_list)
        option = self.find_element(*LoyalLocators.CHOOSE_CARD_AS_ID)
        self.click(option)

    def fill_bonus_card_field(self):
        field = self.find_element(*LoyalLocators.ID_INPUT_FIELD)
        field.send_keys(self.order.user_card)

    def fill_amount_bonus_field(self):
        field = self.find_element(*LoyalLocators.AMOUNT_BONUS_FIELD)
        field.send_keys('100000')

    def fill_operation_details_field(self):
        field = self.find_element(*LoyalLocators.OPERATION_DETAILS_FIELD)
        field.send_keys("Тест")

    def click_apply_button(self):
        apply_button = self.find_element(*LoyalLocators.APPLY_BUTTON)
        self.click(apply_button)

    def check_transaction_is_complete(self):
        self.is_element_present(*LoyalLocators.SUCCESS_TRANSACTION, 25)

    def deposit_ops(self):
        if int(self.order.bonuses_balance) < 10000:
            with allure.step('Начисляем бонусы'):
                self.go_to_deposit_page()
                self.choose_accrual_option()
                self.select_company()
                self.select_currency()
                self.fill_description_field()
                self.fill_internal_description_field()
                self.choose_manual_input_option()
                self.select_id_in_list()
                self.fill_bonus_card_field()
                self.fill_amount_bonus_field()
                self.fill_operation_details_field()
                self.click_apply_button()
                self.check_transaction_is_complete()


