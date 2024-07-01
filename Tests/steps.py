import allure
from API import choose_item_in_catalog, order_submit
from Bitrix.bitrix import Bitrix
from Loymax import login_page, user_page, call_center
from Front_base.locators_front import LoyalLocators
import json
import time


def choose_item(user):
    with allure.step("Выбор товара"):
        search_item = choose_item_in_catalog.ChooseItem(user)
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


def choose_two_items(user):
    choose_item(user)
    choose_item(user)


def submit_and_pay(user, bonuses=False):
    with allure.step("Оформление заказа и выбор оплаты"):
        submit = order_submit.OrderSubmit(user)
        with allure.step("Открываем корзину"):
            submit.open_cart()
        with allure.step("Просматриваем данные заказа для корзины"):
            submit.cart_order_data()
        if bonuses:
            with allure.step("Применяем бонусы: АПИ"):
                submit.use_bonuses()
        with allure.step("Оформляем заказ"):
            submit.add_item_and_order_submit()
            with allure.step("Тело ответа"):
                allure.attach(json.dumps(submit.order_submit_response, indent=2), "API Response",
                              allure.attachment_type.JSON)
        if bonuses:
            with allure.step("Применяем бонусы: Лоялти"):
                pay_bonuses = order_submit.WriteOff(submit.order_submit_response, submit.bonuses, user.user_card)
                pay_bonuses.send_bonuses()
    submit.get_order_number()
    with allure.step(f"Номер заказа: {submit.order_number}"):
        return submit.order_number


def buyout_and_status_change(driver, order_number, status):
    with allure.step("Обработка заказа в Битрикс"):
        bitrix_ops = Bitrix(driver, order_number)
        with allure.step("Авторизуемся в Битрикс"):
            bitrix_ops.authorization()
        with allure.step('Переходим в "Изменить заказ"'):
            bitrix_ops.open(bitrix_ops.order_edit_link())
        with allure.step('Меняем статус выкупа товара на "Да"'):
            bitrix_ops.change_buyout_status_to_yes()
        with allure.step('Открываем страницу заказа'):
            bitrix_ops.open(bitrix_ops.order_link())
        if status == "OI":
            time.sleep(60)
        with allure.step(f'Меняем статус заказа на {status}'):
            bitrix_ops.order_status_change(status)


def loymax_ops(driver, user_with_card):
    with allure.step("Авторизация в Loymax"):
        login_Page = login_page.LoymaxLoginPage(driver)
        with allure.step('Авторизуемся в Loymax'):
            login_Page.authorization()
        with allure.step('Переходим в поиск'):
            call_center_page = call_center.CallCenterPage(driver)
            call_center_page.go_to_search()
        with allure.step('Ищем пользователя'):
            call_center_page.search_user(user_with_card.phone_number[1:])
        with allure.step('Открываем профиль пользователя'):
            user_Page = user_page.UserPage(driver)
        with allure.step('Открываем историю пользователя'):
            user_Page.open_purchase_history()
            user_Page.get_history_screenshot()
        return user_Page





def asserts_delivered_no_bonus_have_card(history_page, order_number):
    with allure.step('Проверки в Loymax'):
        with allure.step('Есть номер заказа'):
            history_page.order_number_is_instance(order_number)
        with allure.step('Заказ подтвержден'):
            history_page.confirmation_check()
        with allure.step('Открываем заказ'):
            history_page.open_loupe()
        with allure.step('Есть строка "Бонус"'):
            history_page.check_text_bonus()
        with allure.step('Зачисление бонусов подтверждено'):
            history_page.check_added_bonus_confirm()
        with allure.step('Зачислено больше нуля бонусов'):
            history_page.check_added_bonuses_count_larger_than_null()


def asserts_delivered_pay_bonus_have_card(history_page, order_number):
    with allure.step('Проверки в Loymax'):
        with allure.step('Есть номер заказа'):
            history_page.order_number_is_instance(order_number)
        with allure.step('Заказ подтвержден'):
            history_page.confirmation_check()
        with allure.step('Открываем заказ'):
            history_page.open_loupe()
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
    # добавить проверки на списание


def asserts_refused_no_bonus_have_card(history_page, order_number):
    with allure.step('Проверки в Loymax'):
        with allure.step('Есть номер заказа'):
            history_page.order_number_is_instance(order_number)
        with allure.step('Заказ отменен'):
            history_page.cancellation_check()


def asserts_refused_pay_bonus_have_card(history_page, order_number):
    with allure.step('Проверки в Loymax'):
        with allure.step('Есть номер заказа'):
            history_page.order_number_is_instance(order_number)
        with allure.step('Заказ отменен'):
            history_page.cancellation_check()


def asserts_cancelled_no_bonus_have_card(history_page, order_number):
    with allure.step('Проверки в Loymax'):
        with allure.step('Есть номер заказа'):
            history_page.order_number_is_instance(order_number)
        with allure.step('Заказ отменен'):
            history_page.cancellation_check()


def asserts_cancelled_pay_bonus_have_card(history_page, order_number):
    with allure.step('Проверки в Loymax'):
        with allure.step('Есть номер заказа'):
            history_page.order_number_is_instance(order_number)
        with allure.step('Заказ отменен'):
            history_page.cancellation_check()


def asserts_processed_pay_bonus_have_card(history_page, order_number):
    with allure.step('Проверки в Loymax'):
        with allure.step('Есть номер заказа'):
            history_page.order_number_is_instance(order_number)
        with allure.step('Песочные часы на месте'):
            history_page.creation_check()
        #проверки на списание?


def asserts_partial_cancelled_no_bonus_have_card(history_page, order_number):
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
        with allure.step('Есть строка "Бонус"'):
            history_page.check_text_bonus()
        with allure.step('Зачисление бонусов подтверждено'):
            history_page.check_added_bonus_confirm()
        with allure.step('Зачислено больше нуля бонусов'):
            history_page.check_added_bonuses_count_larger_than_null()


def asserts_partial_cancelled_pay_bonus_have_card(history_page, order_number):
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