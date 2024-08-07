import allure
from API import catalog, order
from API.authorization import retry
from Bitrix.bitrix import Bitrix
from Loymax import deposit_page, login_page, user_page, call_center
from Front_base.locators_front import LoyalLocators
import pytest
import json
import time


def promocode_parametrize():
    return pytest.mark.parametrize("promocode", [
        pytest.param(False, marks=pytest.mark.no_promocode),
        pytest.param(True, marks=pytest.mark.with_promocode)
    ])


class LoyaltyTestBase:

    def __init__(self, promocode, driver, bonuses=False):
        self.driver = driver
        self.promocode_status = promocode
        self.bonuses_status = bonuses
        self.order = None

    def choose_item(self, user):
        search_item = catalog.ChooseItem(user)
        search_item.catalog_works()

    def choose_two_items(self, user):
        self.choose_item(user)
        self.choose_item(user)

    def filling_out_order_data(self, user):
        with allure.step("Заполнение данных, выбор оплаты"):
            submit = order.Order(user)
            with allure.step("Открываем корзину"):
                submit.open_cart()
            with allure.step("Устанавливаем город"):
                submit.set_city()
            with allure.step("Заполняем данные пользователя"):
                submit.set_order_customer()
            with allure.step('Устанавливаем способ доставки: "Самовывоз"'):
                submit.set_delivery_type_as_pickup()
            with allure.step("Фиксируем ПВЗ"):
                submit.set_pickup_point()
            with allure.step('Устанавливаем способ оплаты: "Наличными при получении"'):
                submit.set_payment_by_cash()
            with allure.step("Просматриваем данные заказа для корзины"):
                submit.cart_order_data()
            if self.promocode_status:
                with allure.step("Применяем промокод"):
                    submit.use_promocode()
                    with allure.step("Тело ответа"):
                        allure.attach(json.dumps(submit.use_promocode_response, indent=2), "API Response",
                                      allure.attachment_type.JSON)

    @retry(3, 0)
    def order_submit(self, user):
        with allure.step("Заполнение данных, выбор оплаты"):
            submit = order.Order(user)
        if self.bonuses_status:
            self.bonuses_ops(submit, user)
        with allure.step("Оформляем заказ"):
            submit.add_item_and_order_submit()
            with allure.step("Тело ответа"):
                allure.attach(json.dumps(submit.order_submit_response, indent=2), "API Response",
                              allure.attachment_type.JSON)
            order_number = submit.get_order_number()
        with allure.step(f"Номер заказа: {order_number}"):
            self.order = submit

    def buyout_and_status_change(self, status):
        with allure.step("Обработка заказа в Битрикс"):
            bitrix_ops = Bitrix(self.driver, self.order)
            with allure.step("Авторизуемся в Битрикс"):
                bitrix_ops.authorization()
            with allure.step('Переходим в "Изменить заказ"'):
                bitrix_ops.open(bitrix_ops.order_edit_link())
            with allure.step('Меняем статус выкупа товара на "Да"'):
                bitrix_ops.change_buyout_status_to_yes()
            with allure.step('Открываем страницу заказа'):
                bitrix_ops.open(bitrix_ops.order_link())
            if self.promocode_status:
                with allure.step('Проверяем, что промокод отображается"'):
                    bitrix_ops.check_promocode_exists()
                with allure.step('Проверяем что сумма заказа совпадает с суммой после применения промокода'):
                    bitrix_ops.check_order_sum_with_promo()
            if status == "OI":
                time.sleep(60)
            with allure.step(f'Меняем статус заказа на {status}'):
                bitrix_ops.order_status_change(status)

    def loymax_ops(self, user_with_card):
        with allure.step("Авторизация в Loymax"):
            login_Page = login_page.LoymaxLoginPage(self.driver)
            with allure.step('Авторизуемся в Loymax'):
                login_Page.authorization()
            if self.bonuses_status:
                with allure.step('Начисляем бонусы'):
                    deposit_Page = deposit_page.DepositPage(self.driver, user_with_card)
                    deposit_Page.deposit_ops()
            with allure.step('Переходим в поиск'):
                call_center_page = call_center.CallCenterPage(self.driver)
                call_center_page.go_to_search()
            with allure.step('Ищем пользователя'):
                call_center_page.search_user(user_with_card.phone_number[1:])
            with allure.step('Открываем профиль пользователя'):
                user_Page = user_page.UserPage(self.driver, self.order)
            with allure.step('Открываем историю пользователя'):
                user_Page.open_purchase_history()
                user_Page.get_history_screenshot()
            return user_Page

    def asserts_delivered_no_bonus_have_card(self, history_page):
        with allure.step('Проверки в Loymax'):
            with allure.step('Есть номер заказа'):
                history_page.order_number_is_instance()
            with allure.step('Заказ подтвержден'):
                history_page.confirmation_check()
            with allure.step('Открываем заказ'):
                history_page.open_loupe()
            if self.promocode_status:
                with allure.step('Промокод на месте'):
                    history_page.check_used_promocode_is_exist()
                with allure.step('Сумма после применения купона совпадает с суммой в лоймаксе'):
                    history_page.check_order_sum_with_promo()
            with allure.step('Есть строка "Бонус"'):
                history_page.check_text_bonus()
            with allure.step('Зачисление бонусов подтверждено'):
                history_page.check_added_bonus_confirm()
            with allure.step('Зачислено больше нуля бонусов'):
                history_page.check_added_bonuses_count_larger_than_null()

    def asserts_delivered_pay_bonus_have_card(self, history_page):
        with allure.step('Проверки в Loymax'):
            with allure.step('Есть номер заказа'):
                history_page.order_number_is_instance()
            with allure.step('Заказ подтвержден'):
                history_page.confirmation_check()
            with allure.step('Открываем заказ'):
                history_page.open_loupe()
            if self.promocode_status:
                with allure.step('Промокод на месте'):
                    history_page.check_used_promocode_is_exist()
                with allure.step('Сумма после применения купона совпадает с суммой в лоймаксе'):
                    history_page.check_order_sum_with_promo()
            with allure.step('Есть строка "Бонус"'):
                history_page.check_text_bonus()
            with allure.step('Зачисление бонусов подтверждено'):
                history_page.check_added_bonus_confirm()
            with allure.step('Зачислено больше нуля бонусов'):
                history_page.check_added_bonuses_count_larger_than_null()
            with allure.step('Списание бонусов подтверждено'):
                history_page.check_paid_bonus_confirmed()
            with allure.step('Списано больше нуля бонусов'):
                history_page.check_paid_bonuses_count_less_than_null()

    def asserts_refused_no_bonus_have_card(self, history_page, order_number, promocode=None):
        with allure.step('Проверки в Loymax'):
            with allure.step('Есть номер заказа'):
                history_page.order_number_is_instance(order_number)
            with allure.step('Заказ отменен'):
                history_page.cancellation_check()
            if promocode:
                with allure.step('Открываем заказ'):
                    history_page.open_loupe()
                with allure.step('Промокод на месте'):
                    history_page.check_used_promocode_is_exist(promocode)
                with allure.step('Сумма после применения купона совпадает с суммой в лоймаксе'):
                    history_page.check_order_sum_with_promo(promocode)

    def asserts_refused_pay_bonus_have_card(self, history_page, order_number, promocode=None):
        with allure.step('Проверки в Loymax'):
            with allure.step('Есть номер заказа'):
                history_page.order_number_is_instance(order_number)
            with allure.step('Заказ отменен'):
                history_page.cancellation_check()
            with allure.step('Открываем заказ'):
                history_page.open_loupe()
            with allure.step('Списание бонусов отменено'):
                history_page.check_paid_bonus_cancelled()
            with allure.step('Отменено списание более чем 0 бонусов'):
                history_page.check_paid_bonuses_count_less_than_null()
            if promocode:
                with allure.step('Промокод на месте'):
                    history_page.check_used_promocode_is_exist(promocode)
                with allure.step('Сумма после применения купона совпадает с суммой в лоймаксе'):
                    history_page.check_order_sum_with_promo(promocode)

    def asserts_cancelled_no_bonus_have_card(self, history_page, order_number):
        with allure.step('Проверки в Loymax'):
            with allure.step('Есть номер заказа'):
                history_page.order_number_is_instance(order_number)
            with allure.step('Заказ отменен'):
                history_page.cancellation_check()

    def asserts_cancelled_pay_bonus_have_card(self, history_page, order_number):
        with allure.step('Проверки в Loymax'):
            with allure.step('Есть номер заказа'):
                history_page.order_number_is_instance(order_number)
            with allure.step('Заказ отменен'):
                history_page.cancellation_check()
            with allure.step('Открываем заказ'):
                history_page.open_loupe()
            with allure.step('Списание бонусов отменено'):
                history_page.check_paid_bonus_cancelled()
            with allure.step('Отменено списание более чем 0 бонусов'):
                history_page.check_paid_bonuses_count_less_than_null()

    def asserts_processed_pay_bonus_have_card(self, history_page, order_number):
        with allure.step('Проверки в Loymax'):
            with allure.step('Есть номер заказа'):
                history_page.order_number_is_instance(order_number)
            with allure.step('Песочные часы на месте'):
                history_page.creation_check()
            #проверки на списание?

    def asserts_partial_cancelled_no_bonus_have_card(self, history_page, order_number, promocode=None):
        with allure.step('Проверки в Loymax'):
            with allure.step('Есть номер заказа'):
                history_page.order_number_is_instance(order_number)
            with allure.step('У заказа два статуса'):
                history_page.partial_cancel_two_statuses_check()
            with allure.step('Первый статус - галка'):
                history_page.confirmation_check()
            with allure.step('Второй статус - крестик'):
                history_page.partial_cancel_cancellation_check()
            with allure.step('Открываем заказ'):
                history_page.open_loupe()
            if promocode:
                with allure.step('Промокод на месте'):
                    history_page.check_used_promocode_is_exist(promocode)
            with allure.step('Есть строка "Бонус"'):
                history_page.check_text_bonus()
            with allure.step('Зачисление бонусов подтверждено'):
                history_page.check_added_bonus_confirm()
            with allure.step('Зачислено больше нуля бонусов'):
                history_page.check_added_bonuses_count_larger_than_null()
            with allure.step('Возвращаемся в историю пользователя'):
                history_page.from_purchase_back_to_history()
            with allure.step('Открываем второй заказ'):
                history_page.second_purchase_open_loup()
            if promocode:
                with allure.step('Промокод на месте'):
                    history_page.check_used_promocode_is_exist(promocode)
                with allure.step('Сумма после применения купона совпадает с суммой в лоймаксе'):
                    history_page.check_order_sum_with_promo(promocode)

    def asserts_partial_cancelled_pay_bonus_have_card(self, history_page, order_number, promocode=None):
        with allure.step('Проверки в Loymax'):
            with allure.step('Есть номер заказа'):
                history_page.order_number_is_instance(order_number)
            with allure.step('У заказа два статуса'):
                history_page.partial_cancel_two_statuses_check()
            with allure.step('Первый статус - галка'):
                history_page.confirmation_check()
            with allure.step('Второй статус - крестик'):
                history_page.partial_cancel_cancellation_check()
            with allure.step('Открываем заказ'):
                history_page.open_loupe()
            if promocode:
                with allure.step('Промокод на месте'):
                    history_page.check_used_promocode_is_exist(promocode)
            with allure.step('Есть строка "Бонус"'):
                history_page.check_text_bonus()
            with allure.step('Зачисление бонусов подтверждено'):
                history_page.check_added_bonus_confirm()
            with allure.step('Зачислено больше нуля бонусов'):
                history_page.check_added_bonuses_count_larger_than_null()
            with allure.step('Списание бонусов подтверждено'):
                history_page.check_paid_bonus_confirmed()
            with allure.step('Списано больше нуля бонусов'):
                history_page.check_paid_bonuses_count_less_than_null()
            with allure.step('Возвращаемся в историю пользователя'):
                history_page.from_purchase_back_to_history()
            with allure.step('Открываем второй заказ'):
                history_page.second_purchase_open_loup()
            if promocode:
                with allure.step('Промокод на месте'):
                    history_page.check_used_promocode_is_exist(promocode)
                with allure.step('Сумма после применения купона совпадает с суммой в лоймаксе'):
                    history_page.check_order_sum_with_promo(promocode)
            with allure.step('Списание бонусов отменено'):
                history_page.check_paid_bonus_cancelled()
            with allure.step('Отменено списание более чем 0 бонусов'):
                history_page.check_paid_bonuses_count_less_than_null()

    def bonuses_ops(self, submit, user):
        with allure.step("Применяем бонусы: API"):
            self.order = submit
            result = submit.use_bonuses()
            retries = 0
            max_retries = 4

            def handle_bad_result(res):
                print("Ошибка: бонусы не применяются.")
                with allure.step("Списание бонусов недоступно для корзины. Пробуем снова"):
                    submit.reset_cart()
                    submit.reset_order()
                    if res[1] == 1:
                        self.choose_item(user)
                    elif res[1] == 2:
                        self.choose_two_items(user)
                    if res[0] == "not available bonuses":
                        print('Начисляем бонусы вручную')
                        deposit_Page = deposit_page.DepositPage(self.driver, submit)
                        print('Переходим на сайт для начисления бонусов')
                        login_Page = login_page.LoymaxLoginPage(self.driver)
                        with allure.step('Авторизуемся в Loymax'):
                            login_Page.authorization()
                        with allure.step('Начисляем бонусы'):
                            deposit_Page.deposit_ops()

            while retries < max_retries:
                if isinstance(result, list):
                    handle_bad_result(result)
                    result = submit.use_bonuses()
                    retries += 1
                else:
                    break
