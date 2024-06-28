import pytest
import allure
from API import choose_item_in_catalog, order_submit
from Bitrix.bitrix import Bitrix
from Loymax import login_page, user_page, call_center
import json
import time


# LGC-T2332 "Доставлен" без баллов Оплата "Наличными при получении" Пользователь без бонусной карты
@allure.issue("https://jira.pochtavip.com/secure/Tests.jspa#/testCase/LGC-T2332", "LGC-T2332")
@allure.feature("Доставлен")
@allure.story('Тест: "Доставлен" без бонусной карты, оплата наличными при получении')
@pytest.mark.no_card
@pytest.mark.delivered
def test_delivered_no_bonus_pay_cash_no_bonus_card(user_no_card, driver):
    with allure.step(f"Пользователь {user_no_card.phone_number}"):
        search_item = choose_item_in_catalog.ChooseItem(user_no_card)
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
    with allure.step("Оформление заказа и выбор оплаты"):
        submit = order_submit.OrderSubmit(user_no_card)
        with allure.step("Открываем корзину"):
            submit.open_cart()
        with allure.step("Просматриваем данные заказа для корзины"):
            submit.cart_order_data()
        ## !!! Шаг 11: Вводим ФИО и номер и почту. Заполняем данные оформления заказа покупателя. POST/order/customer
        ## !!! Шаг 12: Заполнить Город доставки POST/city
        ## !!! Шаг 13: Выбрать способ доставки и указать адрес или ПВЗ.Заполняем данные оформления заказа "Доставка". POST/order/delivery GET/city/address/search POST/order/address
        ## !!! Шаг 14: Выбрать службу доставки и актуальный слот доставки POST/order/address
        ## !!! Шаг 15: Тап на оформление заказа GET/cart/order
        ## !!! Шаг 16: Выбираем оплату Наличными при получении POST/order/payment
        with allure.step("Оформляем заказ"):
            submit.add_item_and_order_submit()
            with allure.step("Тело ответа"):
                allure.attach(json.dumps(submit.order_submit_response, indent=2), "API Response",
                              allure.attachment_type.JSON)
            submit.get_order_number()
    with allure.step(f"Номер заказа: {submit.order_number}"):
        order_number = submit.order_number
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
        with allure.step('Меняем статус заказа на "Доставлен"'):
            bitrix_ops.order_status_change("NI")


# LGC-T2337 "Доставлен" без баллов Оплата "Наличными при получении" Пользователь с бонусной картой
@allure.issue("https://jira.pochtavip.com/secure/Tests.jspa#/testCase/LGC-T2337", "LGC-T2337")
@allure.feature("Доставлен")
@allure.story('Тест: "Доставлен" без баллов, с картой, оплата наличными при получении')
@pytest.mark.with_card
@pytest.mark.delivered
def test_delivered_no_bonus_pay_cash_have_bonus_card(user_with_card, driver):
    with allure.step(f"Пользователь {user_with_card.phone_number}\nКарта {user_with_card.user_card}"):
        search_item = choose_item_in_catalog.ChooseItem(user_with_card)
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
    with allure.step("Оформление заказа и выбор оплаты"):
        submit = order_submit.OrderSubmit(user_with_card)
        with allure.step("Открываем корзину"):
            submit.open_cart()
        with allure.step("Просматриваем данные заказа для корзины"):
            submit.cart_order_data()
        with allure.step("Оформляем заказ"):
            submit.add_item_and_order_submit()
            with allure.step("Тело ответа"):
                allure.attach(json.dumps(submit.order_submit_response, indent=2), "API Response", allure.attachment_type.JSON)
            submit.get_order_number()
    with allure.step(f"Номер заказа: {submit.order_number}"):
        order_number = submit.order_number
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
        with allure.step('Меняем статус заказа на "Доставлен"'):
            bitrix_ops.order_status_change("NI")
    with allure.step("Проверка заказа в Loymax"):
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
        with allure.step('Есть номер заказа'):
            user_Page.order_number_is_instance(order_number)
        with allure.step('Заказ подтвержден'):
            user_Page.confirmation_check()
        with allure.step('Открываем заказ'):
            user_Page.open_loupe()
        with allure.step('Есть строка "Бонус"'):
            user_Page.check_text_bonus()
        with allure.step('Зачисление бонусов подтверждено'):
            user_Page.check_bonus_confirm()
        with allure.step('Зачислено больше нуля бонусов'):
            user_Page.check_added_bonuses_count_larger_than_null()


# LGC-T2348 "Доставлен" с баллами Оплата "Наличными при получении" Пользователь с бонусной картой
@allure.issue("https://jira.pochtavip.com/secure/Tests.jspa#/testCase/LGC-T2348", "LGC-T2348")
@allure.feature("Доставлен")
@allure.story('Тест: "Доставлен" со списанием бонусов, с картой, оплата наличными при получении')
@pytest.mark.with_card
@pytest.mark.with_bonuses
@pytest.mark.delivered
def test_delivered_with_bonus_pay_cash(user_with_card, driver):
    with allure.step(f"Пользователь {user_with_card.phone_number}\nКарта {user_with_card.user_card}"):
        search_item = choose_item_in_catalog.ChooseItem(user_with_card)
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
    with allure.step("Оформление заказа и выбор оплаты"):
        submit = order_submit.OrderSubmit(user_with_card)
        with allure.step("Открываем корзину"):
            submit.open_cart()
        with allure.step("Просматриваем данные заказа для корзины"):
            submit.cart_order_data()
            with allure.step("Тело ответа"):
                allure.attach(json.dumps(submit.cart_data.json(), indent=2), "API Response",
                              allure.attachment_type.JSON)
        with allure.step("Применяем бонусы: АПИ"):
            submit.use_bonuses()
            with allure.step("Оформляем заказ"):
                submit.add_item_and_order_submit()
                with allure.step("Тело ответа"):
                    allure.attach(json.dumps(submit.order_submit_response, indent=2), "API Response",
                                  allure.attachment_type.JSON)
                submit.get_order_number()
        with allure.step("Применяем бонусы: Лоялти"):
            pay_bonuses = order_submit.WriteOff(submit.order_submit_response, submit.bonuses, user_with_card.user_card)
            pay_bonuses.send_bonuses()
            with allure.step("Тело ответа"):
                allure.attach(json.dumps(pay_bonuses.write_off_response, indent=2), "API Response",
                              allure.attachment_type.JSON)
    with allure.step(f"Номер заказа: {submit.order_number}"):
        order_number = submit.order_number

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
        with allure.step('Меняем статус заказа на "Доставлен"'):
            bitrix_ops.order_status_change("NI")

    with allure.step("Проверка заказа в Loymax"):
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
        with allure.step('Есть номер заказа'):
            user_Page.order_number_is_instance(order_number)
        with allure.step('Заказ подтвержден'):
            user_Page.confirmation_check()
        with allure.step('Открываем заказ'):
            user_Page.open_loupe()
        with allure.step('Есть строка "Бонус"'):
            user_Page.check_text_bonus()
        with allure.step('Зачисление бонусов подтверждено'):
            user_Page.check_bonus_confirm()
        with allure.step('Зачислено больше нуля бонусов'):
            user_Page.check_added_bonuses_count_larger_than_null()


# LGC-T2346 "Отказ" без баллов Оплата "Наличными при получении" Пользователь с бонусной картой
@allure.issue("https://jira.pochtavip.com/secure/Tests.jspa#/testCase/LGC-T2346", "LGC-T2346")
@allure.feature("Отказ")
@allure.story('Тест: "Отказ" без баллов, с картой, оплата наличными при получении')
@pytest.mark.with_card
@pytest.mark.refused
def test_refused_no_bonus_pay_cash_have_bonus_card(user_with_card, driver):
    with allure.step(f"Пользователь {user_with_card.phone_number}\nКарта {user_with_card.user_card} "):
        search_item = choose_item_in_catalog.ChooseItem(user_with_card)
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
    with allure.step("Оформление заказа и выбор оплаты"):
        submit = order_submit.OrderSubmit(user_with_card)
        with allure.step("Открываем корзину"):
            submit.open_cart()
        with allure.step("Просматриваем данные заказа для корзины"):
            submit.cart_order_data()
        with allure.step("Оформляем заказ"):
            submit.add_item_and_order_submit()
            with allure.step("Тело ответа"):
                allure.attach(json.dumps(submit.order_submit_response, indent=2), "API Response",
                              allure.attachment_type.JSON)
            submit.get_order_number()
    with allure.step(f"Номер заказа: {submit.order_number}"):
        order_number = submit.order_number
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
        with allure.step('Меняем статус заказа на "Отказ"'):
            bitrix_ops.order_status_change("QI")

    with allure.step("Проверка заказа в Loymax"):
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
        with allure.step('Есть номер заказа'):
            user_Page.order_number_is_instance(order_number)
        with allure.step('Заказ отменен'):
            user_Page.cancellation_check()


# LGC-T2345 "Отказ" с баллами Оплата "Наличными при получении" Пользователь с бонусной картой
@allure.issue("https://jira.pochtavip.com/secure/Tests.jspa#/testCase/LGC-T2345", "LGC-T2345")
@allure.feature("Отказ")
@allure.story('Тест: "Отказ" со списанием бонусов, с картой, оплата наличными при получении')
@pytest.mark.with_card
@pytest.mark.with_bonuses
@pytest.mark.refused
def test_refused_with_bonus_pay_cash(user_with_card, driver):
    with allure.step(f"Пользователь {user_with_card.phone_number}\nКарта {user_with_card.user_card} "):
        search_item = choose_item_in_catalog.ChooseItem(user_with_card)
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
    with allure.step("Оформление заказа и выбор оплаты"):
        submit = order_submit.OrderSubmit(user_with_card)
        with allure.step("Открываем корзину"):
            submit.open_cart()
        with allure.step("Просматриваем данные заказа для корзины"):
            submit.cart_order_data()
        with allure.step("Применяем бонусы: АПИ"):
            submit.use_bonuses()
            with allure.step("Оформляем заказ"):
                submit.add_item_and_order_submit()
                with allure.step("Тело ответа"):
                    allure.attach(json.dumps(submit.order_submit_response, indent=2), "API Response",
                                  allure.attachment_type.JSON)
                submit.get_order_number()
        with allure.step("Применяем бонусы: Лоялти"):
            pay_bonuses = order_submit.WriteOff(submit.order_submit_response, submit.bonuses, user_with_card.user_card)
            pay_bonuses.send_bonuses()
            with allure.step("Тело ответа"):
                allure.attach(json.dumps(pay_bonuses.write_off_response, indent=2), "API Response",
                              allure.attachment_type.JSON)
    with allure.step(f"Номер заказа: {submit.order_number}"):
        order_number = submit.order_number

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
        with allure.step('Меняем статус заказа на "Отказ"'):
            bitrix_ops.order_status_change("QI")

    with allure.step("Проверка заказа в Loymax"):
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
        with allure.step('Есть номер заказа'):
            user_Page.order_number_is_instance(order_number)
        with allure.step('Заказ отменен'):
            user_Page.cancellation_check()


# LGC-T2344 "Отмена" без баллов Оплата "Наличными при получении" Пользователь с бонусной картой
@allure.issue("https://jira.pochtavip.com/secure/Tests.jspa#/testCase/LGC-T2344", "LGC-T2344")
@allure.feature("Отмена")
@allure.story('Тест: "Отмена" без баллов, с картой, оплата наличными при получении')
@pytest.mark.with_card
@pytest.mark.cancelled
def test_cancelled_no_bonus_pay_cash(user_with_card, driver):
    with allure.step(f"Пользователь {user_with_card.phone_number}\nКарта {user_with_card.user_card} "):
        search_item = choose_item_in_catalog.ChooseItem(user_with_card)
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
    with allure.step("Оформление заказа и выбор оплаты"):
        submit = order_submit.OrderSubmit(user_with_card)
        with allure.step("Открываем корзину"):
            submit.open_cart()
        with allure.step("Просматриваем данные заказа для корзины"):
            submit.cart_order_data()
        with allure.step("Оформляем заказ"):
            submit.add_item_and_order_submit()
            with allure.step("Тело ответа"):
                allure.attach(json.dumps(submit.order_submit_response, indent=2), "API Response",
                              allure.attachment_type.JSON)
            submit.get_order_number()
    with allure.step(f"Номер заказа: {submit.order_number}"):
        order_number = submit.order_number
    with allure.step("Обработка заказа в Битрикс"):
        bitrix_ops = Bitrix(driver, order_number)
        with allure.step("Авторизуемся в Битрикс"):
            bitrix_ops.authorization()
        with allure.step('Открываем страницу заказа'):
            bitrix_ops.open(bitrix_ops.order_link())
        with allure.step('Меняем статус заказа на "Отмена"'):
            bitrix_ops.order_status_change("MB")

    with allure.step("Проверка заказа в Loymax"):
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
        with allure.step('Есть номер заказа'):
            user_Page.order_number_is_instance(order_number)
        with allure.step('Заказ отменен'):
            user_Page.cancellation_check()


# LGC-T2335 "Отмена" с баллами Оплата "Наличными при получении" Пользователь с бонусной картой
@allure.issue("https://jira.pochtavip.com/secure/Tests.jspa#/testCase/LGC-T2335", "LGC-T2335")
@allure.feature("Отмена")
@allure.story('Тест: "Отмена" со списанием бонусов, с картой, оплата наличными при получении')
@pytest.mark.with_card
@pytest.mark.with_bonuses
@pytest.mark.cancelled
def test_cancelled_with_bonus_pay_cash(user_with_card, driver):
    with allure.step(f"Пользователь {user_with_card.phone_number}\nКарта {user_with_card.user_card} "):
        search_item = choose_item_in_catalog.ChooseItem(user_with_card)
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
    with allure.step("Оформление заказа и выбор оплаты"):
        submit = order_submit.OrderSubmit(user_with_card)
        with allure.step("Открываем корзину"):
            submit.open_cart()
        with allure.step("Просматриваем данные заказа для корзины"):
            submit.cart_order_data()
    with allure.step("Применяем бонусы: АПИ"):
        submit.use_bonuses()
        with allure.step("Оформляем заказ"):
            submit.add_item_and_order_submit()
            with allure.step("Тело ответа"):
                allure.attach(json.dumps(submit.order_submit_response, indent=2), "API Response",
                              allure.attachment_type.JSON)
            submit.get_order_number()
    with allure.step("Применяем бонусы: Лоялти"):
        pay_bonuses = order_submit.WriteOff(submit.order_submit_response, submit.bonuses, user_with_card.user_card)
        pay_bonuses.send_bonuses()
        with allure.step("Тело ответа"):
            allure.attach(json.dumps(pay_bonuses.write_off_response, indent=2), "API Response",
                          allure.attachment_type.JSON)
    with allure.step(f"Номер заказа: {submit.order_number}"):
        order_number = submit.order_number

    with allure.step("Обработка заказа в Битрикс"):
        bitrix_ops = Bitrix(driver, order_number)
        with allure.step("Авторизуемся в Битрикс"):
            bitrix_ops.authorization()
        with allure.step('Открываем страницу заказа'):
            bitrix_ops.open(bitrix_ops.order_link())
        with allure.step('Меняем статус заказа на "Отмена"'):
            bitrix_ops.order_status_change("MB")

    with allure.step("Проверка заказа в Loymax"):
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
        with allure.step('Есть номер заказа'):
            user_Page.order_number_is_instance(order_number)
        with allure.step('Заказ отменен'):
            user_Page.cancellation_check()


# LGC-T2347 "Оформлен" оплата "Наличными при получении" Пользователь без бонусной карты
@allure.issue("https://jira.pochtavip.com/secure/Tests.jspa#/testCase/LGC-T2347", "LGC-T2347")
@allure.feature("Оформлен")
@allure.story('Тест: "Оформлен" без бонусной карты, оплата наличными при получении')
@pytest.mark.no_card
@pytest.mark.processed
def test_processed_pay_cash_no_bonus_card(user_no_card, driver):  # в черновом варианте - просто оформление заказа
    with allure.step(f"Пользователь {user_no_card.phone_number}"):
        search_item = choose_item_in_catalog.ChooseItem(user_no_card)

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

    with allure.step("Оформление заказа и выбор оплаты"):
        submit = order_submit.OrderSubmit(user_no_card)
        with allure.step("Открываем корзину"):
            submit.open_cart()
        with allure.step("Просматриваем данные заказа для корзины"):
            submit.cart_order_data()
        with allure.step("Оформляем заказ"):
            submit.add_item_and_order_submit()
            with allure.step("Тело ответа"):
                allure.attach(json.dumps(submit.order_submit_response, indent=2), "API Response",
                              allure.attachment_type.JSON)
            submit.get_order_number()
        with allure.step(f"Номер заказа: {submit.order_number}"):
            order_number = submit.order_number

    with allure.step("Обработка заказа в Битрикс"):
        bitrix_ops = Bitrix(driver, order_number)
        with allure.step("Авторизуемся в Битрикс"):
            bitrix_ops.authorization()
        with allure.step('Открываем страницу заказа'):
            bitrix_ops.open(bitrix_ops.order_link())
        with allure.step('Меняем статус заказа на "Оформлен"'):
            bitrix_ops.order_status_change("AB")


@allure.issue("https://jira.pochtavip.com/secure/Tests.jspa#/testCase/LGC-T2341", "LGC-T2341")
@allure.feature("Оформлен")
@allure.story('Тест: "Оформлен" без баллов, с картой, оплата наличными при получении')
@pytest.mark.with_card
@pytest.mark.processed
def test_processed_pay_cash_with_bonus_card(user_with_card, driver):  # в черновом варианте - просто оформление заказа

    with allure.step(f"Пользователь {user_with_card.phone_number}\nКарта {user_with_card.user_card} "):
        search_item = choose_item_in_catalog.ChooseItem(user_with_card)
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
    with allure.step("Оформление заказа и выбор оплаты"):
        submit = order_submit.OrderSubmit(user_with_card)
        with allure.step("Открываем корзину"):
            submit.open_cart()
        with allure.step("Просматриваем данные заказа для корзины"):
            submit.cart_order_data()
        with allure.step("Оформляем заказ"):
            submit.add_item_and_order_submit()
            with allure.step("Тело ответа"):
                allure.attach(json.dumps(submit.order_submit_response, indent=2), "API Response",
                              allure.attachment_type.JSON)
            submit.get_order_number()
    with allure.step(f"Номер заказа: {submit.order_number}"):
        order_number = submit.order_number
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
        with allure.step('Меняем статус заказа на "Оформлен"'):
            bitrix_ops.order_status_change("AB")

    # with allure.step("Проверка заказа в Loymax"):
    #     login_Page = login_page.LoymaxLoginPage(driver)
    #     with allure.step('Авторизуемся в Loymax'):
    #         login_Page.authorization()
    #     with allure.step('Переходим в поиск'):
    #         call_center_page = call_center.CallCenterPage(driver)
    #         call_center_page.go_to_search()
    #     with allure.step('Ищем пользователя'):
    #         call_center_page.search_user(user_with_card.phone_number[1:])
    #     with allure.step('Открываем профиль пользователя'):
    #         user_Page = user_page.UserPage(driver)
    #     with allure.step('Открываем историю пользователя'):
    #         user_Page.open_purchase_history()
    #     with allure.step('Есть номер заказа'):
    #         user_Page.order_number_is_instance(order_number)
    #     with allure.step('Песочные часы на месте'):
    #         user_Page.creation_check()


# LGC-T2342 "Оформлен" с баллами Оплата "Наличными при получении" Пользователь с бонусной картой
@allure.issue("https://jira.pochtavip.com/secure/Tests.jspa#/testCase/LGC-T2342", "LGC-T2342")
@allure.feature("Оформлен")
@allure.story('Тест: "Оформлен" со списанием бонусов, с картой, оплата наличными при получении')
@pytest.mark.with_card
@pytest.mark.with_bonuses
@pytest.mark.processed
def test_processed_with_bonus_pay_cash(user_with_card, driver):
    with allure.step(f"Пользователь {user_with_card.phone_number}\nКарта {user_with_card.user_card} "):
        search_item = choose_item_in_catalog.ChooseItem(user_with_card)
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
    with allure.step("Оформление заказа и выбор оплаты"):
        submit = order_submit.OrderSubmit(user_with_card)
        with allure.step("Открываем корзину"):
            submit.open_cart()
        with allure.step("Просматриваем данные заказа для корзины"):
            submit.cart_order_data()
            with allure.step("Тело ответа"):
                allure.attach(json.dumps(submit.cart_data, indent=2), "API Response",
                              allure.attachment_type.JSON)
    with allure.step("Применяем бонусы: АПИ"):
        submit.use_bonuses()
        with allure.step("Оформляем заказ"):
            submit.add_item_and_order_submit()
            with allure.step("Тело ответа"):
                allure.attach(json.dumps(submit.order_submit_response, indent=2), "API Response",
                              allure.attachment_type.JSON)
            submit.get_order_number()
    with allure.step("Применяем бонусы: Лоялти"):
        pay_bonuses = order_submit.WriteOff(submit.order_submit_response, submit.bonuses, user_with_card.user_card)
        pay_bonuses.send_bonuses()
        with allure.step("Тело ответа"):
            allure.attach(json.dumps(pay_bonuses.write_off_response, indent=2), "API Response",
                          allure.attachment_type.JSON)
    with allure.step(f"Номер заказа: {submit.order_number}"):
        order_number = submit.order_number

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
        with allure.step('Меняем статус заказа на "Оформлен"'):
            bitrix_ops.order_status_change("AB")

    with allure.step("Проверка заказа в Loymax"):
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
        with allure.step('Есть номер заказа'):
            user_Page.order_number_is_instance(order_number)
        with allure.step('Песочные часы на месте'):
            user_Page.creation_check()


# LGC-T2334 "Частичный отказ" без баллов Оплата "Наличными при получении" в корзине 2 товара Пользователь без бонусной карты
@allure.issue("https://jira.pochtavip.com/secure/Tests.jspa#/testCase/LGC-T2334", "LGC-T2334")
@allure.feature("Частичный отказ")
@allure.story('Тест: "Частичный отказ" без бонусной карты, оплата наличными при получении')
@pytest.mark.no_card
@pytest.mark.partial_cancelled
def test_partial_cancelled_pay_cash_no_bonus_card(user_no_card, driver):
    with allure.step(f"Пользователь {user_no_card.phone_number}"):
        search_item = choose_item_in_catalog.ChooseItem(user_no_card)
    with allure.step("Выбор первого товара"):
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
    with allure.step("Выбор второго товара"):
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

    with allure.step("Оформление заказа и выбор оплаты"):
        submit = order_submit.OrderSubmit(user_no_card)
        with allure.step("Открываем корзину"):
            submit.open_cart()
        with allure.step("Просматриваем данные заказа для корзины"):
            submit.cart_order_data()
        with allure.step("Оформляем заказ"):
            submit.add_item_and_order_submit()
            with allure.step("Тело ответа"):
                allure.attach(json.dumps(submit.order_submit_response, indent=2), "API Response",
                              allure.attachment_type.JSON)
            submit.get_order_number()
        with allure.step(f"Номер заказа: {submit.order_number}"):
            order_number = submit.order_number

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
        with allure.step('Меняем статус на "Частичный отказ"'):
            bitrix_ops.order_status_change("OI")


# LGC-T2339 "Частичный отказ" без баллов Оплата "Наличными при получении" в корзине 2 товара Пользователь с бонусной картой
@allure.issue("https://jira.pochtavip.com/secure/Tests.jspa#/testCase/LGC-T2339", "LGC-T2339")
@allure.feature("Частичный отказ")
@allure.story('Тест: "Частичный отказ" без баллов, с картой, оплата наличными при получении')
@pytest.mark.with_card
@pytest.mark.partial_cancelled
def test_partial_cancelled_no_bonus_pay_cash_with_bonus_card(user_with_card, driver):
    with allure.step(f"Пользователь {user_with_card.phone_number}\nКарта {user_with_card.user_card} "):
        search_item = choose_item_in_catalog.ChooseItem(user_with_card)
    with allure.step("Выбор первого товара"):
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
    with allure.step("Выбор второго товара"):
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
    with allure.step("Оформление заказа и выбор оплаты"):
        submit = order_submit.OrderSubmit(user_with_card)
        with allure.step("Открываем корзину"):
            submit.open_cart()
        with allure.step("Просматриваем данные заказа для корзины"):
            submit.cart_order_data()
        with allure.step("Оформляем заказ"):
            submit.add_item_and_order_submit()
            with allure.step("Тело ответа"):
                allure.attach(json.dumps(submit.order_submit_response, indent=2), "API Response",
                              allure.attachment_type.JSON)
            submit.get_order_number()
    with allure.step(f"Номер заказа: {submit.order_number}"):
        order_number = submit.order_number
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
        time.sleep(60)
        with allure.step('Меняем статус на "Частичный отказ"'):
            bitrix_ops.order_status_change("OI")

    with allure.step("Проверка заказа в Loymax"):
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
        with allure.step('У заказа два статуса'):
            user_Page.partial_cancel_two_statuses_check()
        with allure.step('Первый статус - галка'):
            user_Page.confirmation_check()
        with allure.step('Второй статус - крестик'):
            user_Page.partial_cancel_cancellation_check()
        with allure.step('Открываем заказ'):
            user_Page.open_loupe()
        with allure.step('Есть строка "Бонус"'):
            user_Page.check_text_bonus()
        with allure.step('Зачисление бонусов подтверждено'):
            user_Page.check_bonus_confirm()
        with allure.step('Зачислено больше нуля бонусов'):
            user_Page.check_added_bonuses_count_larger_than_null()


# LGC-T2340 "Частичный отказ" с баллами Оплата "Наличными при получении" в корзине 2 товара Пользователь с бонусной картой
@allure.issue("https://jira.pochtavip.com/secure/Tests.jspa#/testCase/LGC-T2340", "LGC-T2340")
@allure.feature("Частичный отказ")
@allure.story('Тест: "Частичный отказ" со списанием бонусов, с картой, оплата наличными при получении')
@pytest.mark.with_card
@pytest.mark.partial_cancelled
def test_partial_cancelled_with_bonus_pay_cash(user_with_card, driver):
    with allure.step(f"Пользователь {user_with_card.phone_number}\nКарта {user_with_card.user_card} "):
        search_item = choose_item_in_catalog.ChooseItem(user_with_card)
    with allure.step("Выбор первого товара"):
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
    with allure.step("Выбор второго товара"):
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
    with allure.step("Оформление заказа и выбор оплаты"):
        submit = order_submit.OrderSubmit(user_with_card)
        with allure.step("Открываем корзину"):
            submit.open_cart()
        with allure.step("Просматриваем данные заказа для корзины"):
            submit.cart_order_data()
        with allure.step("Применяем бонусы: АПИ"):
            submit.use_bonuses()
            with allure.step("Оформляем заказ"):
                submit.add_item_and_order_submit()
                with allure.step("Тело ответа"):
                    allure.attach(json.dumps(submit.order_submit_response, indent=2), "API Response",
                                  allure.attachment_type.JSON)
                submit.get_order_number()
        with allure.step("Применяем бонусы: Лоялти"):
            pay_bonuses = order_submit.WriteOff(submit.order_submit_response, submit.bonuses, user_with_card.user_card)
            pay_bonuses.send_bonuses()
            with allure.step("Тело ответа"):
                allure.attach(json.dumps(pay_bonuses.write_off_response, indent=2), "API Response",
                              allure.attachment_type.JSON)
    with allure.step(f"Номер заказа: {submit.order_number}"):
         order_number = submit.order_number

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
        time.sleep(60)
        with allure.step('Меняем статус на "Частичный отказ"'):
            bitrix_ops.order_status_change("OI")

    with allure.step("Проверка заказа в Loymax"):
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
        with allure.step('У заказа два статуса'):
            user_Page.partial_cancel_two_statuses_check()
        with allure.step('Первый статус - галка'):
            user_Page.confirmation_check()
        with allure.step('Второй статус - крестик'):
            user_Page.partial_cancel_cancellation_check()
        with allure.step('Открываем заказ'):
            user_Page.open_loupe()
        with allure.step('Есть строка "Бонус"'):
            user_Page.check_text_bonus()
        with allure.step('Зачисление бонусов подтверждено'):
            user_Page.check_bonus_confirm()
        with allure.step('Зачислено больше нуля бонусов'):
            user_Page.check_added_bonuses_count_larger_than_null()
