import allure
from API import catalog, order, authorization
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

    def __init__(self, driver, promocode=False, bonuses=False):
        self.driver = driver
        self.promocode_status = promocode
        self.bonuses_status = bonuses
        self.order = None


    def choose_item(self, user):
        print('оппа')
        search_item = catalog.ChooseItem(user)
        with allure.step("Выбор товара"):
            with allure.step("Открываем каталог"):
                search_item.get_catalog()
            with allure.step("Выбираем категорию"):
                search_item.get_category()
            with allure.step("Открываем список товаров"):
                search_item.get_list()
            with allure.step("Открываем карточку товара"):
                search_item.get_item_card_from_product_list()
            with allure.step("Проверяем доступные размеры товара"):
                search_item.check_available_item_sizes()
            with allure.step("Добавляем товар в корзину"):
                search_item.add_item_in_cart()

    def choose_two_items(self, user):
        self.choose_item(user)
        self.choose_item(user)

    def order_submit(self, user):
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
            if self.bonuses_status:
                self.bonuses_ops(submit)
            if self.promocode_status:
                with allure.step("Применяем промокод"):
                    submit.use_promocode()
                    with allure.step("Тело ответа"):
                        allure.attach(json.dumps(submit.use_promocode_response, indent=2), "API Response",
                                      allure.attachment_type.JSON)
            with allure.step("Оформляем заказ"):
                submit.submit_an_order()
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

    def asserts_refused_no_bonus_have_card(self, history_page):
        with allure.step('Проверки в Loymax'):
            with allure.step('Есть номер заказа'):
                history_page.order_number_is_instance()
            with allure.step('Заказ отменен'):
                history_page.cancellation_check()
            if self.promocode_status:
                with allure.step('Открываем заказ'):
                    history_page.open_loupe()
                with allure.step('Промокод на месте'):
                    history_page.check_used_promocode_is_exist()
                with allure.step('Сумма после применения купона совпадает с суммой в лоймаксе'):
                    history_page.check_order_sum_with_promo()

    def asserts_refused_pay_bonus_have_card(self, history_page):
        with allure.step('Проверки в Loymax'):
            with allure.step('Есть номер заказа'):
                history_page.order_number_is_instance()
            with allure.step('Заказ отменен'):
                history_page.cancellation_check()
            with allure.step('Открываем заказ'):
                history_page.open_loupe()
            with allure.step('Списание бонусов отменено'):
                history_page.check_paid_bonus_cancelled()
            with allure.step('Отменено списание более чем 0 бонусов'):
                history_page.check_paid_bonuses_count_less_than_null()
            if self.promocode_status:
                with allure.step('Промокод на месте'):
                    history_page.check_used_promocode_is_exist()
                with allure.step('Сумма после применения купона совпадает с суммой в лоймаксе'):
                    history_page.check_order_sum_with_promo()

    def asserts_cancelled_no_bonus_have_card(self, history_page):
        with allure.step('Проверки в Loymax'):
            with allure.step('Есть номер заказа'):
                history_page.order_number_is_instance()
            with allure.step('Заказ отменен'):
                history_page.cancellation_check()

    def asserts_cancelled_pay_bonus_have_card(self, history_page):
        with allure.step('Проверки в Loymax'):
            with allure.step('Есть номер заказа'):
                history_page.order_number_is_instance()
            with allure.step('Заказ отменен'):
                history_page.cancellation_check()
            with allure.step('Открываем заказ'):
                history_page.open_loupe()
            with allure.step('Списание бонусов отменено'):
                history_page.check_paid_bonus_cancelled()
            with allure.step('Отменено списание более чем 0 бонусов'):
                history_page.check_paid_bonuses_count_less_than_null()

    def asserts_processed_pay_bonus_have_card(self, history_page):
        with allure.step('Проверки в Loymax'):
            with allure.step('Есть номер заказа'):
                history_page.order_number_is_instance()
            with allure.step('Песочные часы на месте'):
                history_page.creation_check()
            #проверки на списание?

    def asserts_partial_cancelled_no_bonus_have_card(self, history_page):
        with allure.step('Проверки в Loymax'):
            with allure.step('Есть номер заказа'):
                history_page.order_number_is_instance()
            with allure.step('У заказа два статуса'):
                history_page.partial_cancel_two_statuses_check()
            with allure.step('Первый статус - галка'):
                history_page.confirmation_check()
            with allure.step('Второй статус - крестик'):
                history_page.partial_cancel_cancellation_check()
            with allure.step('Открываем заказ'):
                history_page.open_loupe()
            if self.promocode_status:
                with allure.step('Промокод на месте'):
                    history_page.check_used_promocode_is_exist()
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
            if self.promocode_status:
                with allure.step('Промокод на месте'):
                    history_page.check_used_promocode_is_exist()
                with allure.step('Сумма после применения купона совпадает с суммой в лоймаксе'):
                    history_page.check_order_sum_with_promo()

    def asserts_partial_cancelled_pay_bonus_have_card(self, history_page):
        with allure.step('Проверки в Loymax'):
            with allure.step('Есть номер заказа'):
                history_page.order_number_is_instance()
            with allure.step('У заказа два статуса'):
                history_page.partial_cancel_two_statuses_check()
            with allure.step('Первый статус - галка'):
                history_page.confirmation_check()
            with allure.step('Второй статус - крестик'):
                history_page.partial_cancel_cancellation_check()
            with allure.step('Открываем заказ'):
                history_page.open_loupe()
            if self.promocode_status:
                with allure.step('Промокод на месте'):
                    history_page.check_used_promocode_is_exist()
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
            if self.promocode_status:
                with allure.step('Промокод на месте'):
                    history_page.check_used_promocode_is_exist()
                with allure.step('Сумма после применения купона совпадает с суммой в лоймаксе'):
                    history_page.check_order_sum_with_promo()
            with allure.step('Списание бонусов отменено'):
                history_page.check_paid_bonus_cancelled()
            with allure.step('Отменено списание более чем 0 бонусов'):
                history_page.check_paid_bonuses_count_less_than_null()

    def bonuses_ops(self, submit):
        with allure.step("Применяем бонусы: API"):

            @retry(3,1)
            def handle_bad_result():
                print("Ошибка: бонусы не применяются.")
                with allure.step("Списание бонусов недоступно для корзины. Пробуем снова"):

                    if submit.check_available_bonuses_is_null():
                        print('Начисляем бонусы вручную')
                        deposit_Page = deposit_page.DepositPage(self.driver, submit)
                        print('Переходим на сайт для начисления бонусов')
                        login_Page = login_page.LoymaxLoginPage(self.driver)
                        with allure.step('Авторизуемся в Loymax'):
                            login_Page.authorization()
                        with allure.step('Начисляем бонусы'):
                            deposit_Page.deposit_ops()
                    if submit.check_max_bonus_is_null():
                        print("less")
                        count_of_items = submit.count_of_items_in_the_cart()
                        print(count_of_items)
                        submit.reset_cart()
                        if count_of_items == 1:
                            self.choose_item(submit.api_client)
                        elif count_of_items == 2:
                            self.choose_two_items(submit.api_client)
            def check():
                if submit.check_available_bonuses_is_null() or submit.check_max_bonus_is_null():
                    print(submit.get_cart)
                    handle_bad_result()
                    submit.open_cart()
                    print(submit.get_cart)
                    check()
            check()
            print("Вроде")
            submit.use_bonuses()
