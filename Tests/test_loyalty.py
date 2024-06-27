import pytest
import allure
from API import choose_item_in_catalog, order_submit
from Bitrix.bitrix import Bitrix
from Loymax import login_page, user_page, call_center

import time


# LGC-T2332 "Доставлен" без баллов Оплата "Наличными при получении" Пользователь без бонусной карты
@allure.issue("https://jira.pochtavip.com/secure/Tests.jspa#/testCase/LGC-T2332", "LGC-T2332")
@allure.feature("Доставлен")
@allure.story('Тест: "Доставлен" без бонусной карты, оплата наличными при получении')
@pytest.mark.no_card
@pytest.mark.delivered
def test_delivered_no_bonus_pay_cash_no_bonus_card(user_no_card, driver):
    with allure.step("Выбор товара и оформление заказа"):
        search_item = choose_item_in_catalog.ChooseItem(user_no_card)
        search_item.get_catalog()
        search_item.get_category()
        search_item.get_item_card_from_product_list()
        search_item.check_available_item_sizes()
        search_item.add_item_in_cart()

    with allure.step("Оформление заказа и выбор оплаты"):
        submit = order_submit.OrderSubmit(user_no_card)
        submit.open_cart()
        submit.cart_order_data()
        ## !!! Шаг 11: Вводим ФИО и номер и почту. Заполняем данные оформления заказа покупателя. POST/order/customer
        ## !!! Шаг 12: Заполнить Город доставки POST/city
        ## !!! Шаг 13: Выбрать способ доставки и указать адрес или ПВЗ.Заполняем данные оформления заказа "Доставка". POST/order/delivery GET/city/address/search POST/order/address
        ## !!! Шаг 14: Выбрать службу доставки и актуальный слот доставки POST/order/address
        ## !!! Шаг 15: Тап на оформление заказа GET/cart/order
        ## !!! Шаг 16: Выбираем оплату Наличными при получении POST/order/payment
        submit.add_item_and_order_submit()
        submit.get_order_number()
        order_number = submit.order_number

    with allure.step("Обработка заказа в CRM"):
        bitrix_ops = Bitrix(driver)
        bitrix_ops.authorization()
        bitrix_ops.open(Bitrix.order_edit_link(order_number))
        bitrix_ops.change_buyout_status_to_yes()
        bitrix_ops.open(Bitrix.order_link(order_number))
        bitrix_ops.order_status_change("NI")



# LGC-T2337 "Доставлен" без баллов Оплата "Наличными при получении" Пользователь с бонусной картой
@allure.issue("https://jira.pochtavip.com/secure/Tests.jspa#/testCase/LGC-T2337", "LGC-T2337")
@allure.feature("Доставлен")
@allure.story('Тест: "Доставлен" без баллов, с картой, оплата наличными при получении')
@pytest.mark.with_card
@pytest.mark.delivered
def test_delivered_no_bonus_pay_cash_have_bonus_card(user_with_card, driver):
    with allure.step("Выбор товара и оформление заказа"):
        search_item = choose_item_in_catalog.ChooseItem(user_with_card)
        search_item.get_catalog()
        search_item.get_category()
        search_item.get_list()
        search_item.get_item_card_from_product_list()
        search_item.check_available_item_sizes()
        search_item.add_item_in_cart()

    with allure.step("Оформление заказа и выбор оплаты"):
        submit = order_submit.OrderSubmit(user_with_card)
        submit.open_cart()
        submit.cart_order_data()
        submit.add_item_and_order_submit()
        submit.get_order_number()
        order_number = submit.order_number

    with allure.step("Обработка заказа в CRM и проверка бонусов"):
        bitrix_ops = Bitrix(driver)
        bitrix_ops.authorization()

        bitrix_ops.open(Bitrix.order_edit_link(order_number))
        bitrix_ops.change_buyout_status_to_yes()
        bitrix_ops.open(Bitrix.order_link(order_number))
        bitrix_ops.order_status_change("NI")

        login_Page = login_page.LoymaxLoginPage(driver)
        login_Page.authorization()
        call_center_page = call_center.CallCenterPage(driver)
        call_center_page.go_to_search()
        call_center_page.search_user(user_with_card.phone_number[1:])
        user_Page = user_page.UserPage(driver)
        user_Page.open_purchase_history()
        user_Page.order_number_is_instance(order_number)
        user_Page.confirmation_check()
        user_Page.open_loupe()
        user_Page.check_text_bonus()
        user_Page.check_bonus_confirm()
        user_Page.check_added_bonuses_count_larger_than_null()




# LGC-T2348 "Доставлен" с баллами Оплата "Наличными при получении" Пользователь с бонусной картой
@allure.issue("https://jira.pochtavip.com/secure/Tests.jspa#/testCase/LGC-T2348", "LGC-T2348")
@allure.feature("Доставлен")
@allure.story('Тест: "Доставлен" со списанием бонусов, с картой, оплата наличными при получении')
@pytest.mark.with_card
@pytest.mark.with_bonuses
@pytest.mark.delivered
def test_delivered_with_bonus_pay_cash(user_with_card, driver):
    with allure.step("Выбор товара и оформление заказа"):
        search_item = choose_item_in_catalog.ChooseItem(user_with_card)
        search_item.get_catalog()
        search_item.get_category()
        search_item.get_item_card_from_product_list()
        search_item.check_available_item_sizes()
        search_item.add_item_in_cart()

    with allure.step("Оформление заказа и выбор оплаты с использованием бонусов"):
        submit = order_submit.OrderSubmit(user_with_card)
        submit.open_cart()
        submit.cart_order_data()
        submit.use_bonuses()
        submit.add_item_and_order_submit()
        submit.get_order_number()
        order_number = submit.order_number

    with allure.step("Обработка заказа в CRM и проверка бонусов"):
        bitrix_ops = Bitrix(driver)
        bitrix_ops.authorization()
        bitrix_ops.open(Bitrix.order_edit_link(order_number))
        bitrix_ops.change_buyout_status_to_yes()
        bitrix_ops.open(Bitrix.order_link(order_number))
        bitrix_ops.order_status_change("NI")

        login_Page = login_page.LoymaxLoginPage(driver)
        login_Page.authorization()
        call_center_page = call_center.CallCenterPage(driver)
        call_center_page.go_to_search()
        call_center_page.search_user(user_with_card.phone_number[1:])
        user_Page = user_page.UserPage(driver)
        user_Page.open_purchase_history()
        user_Page.order_number_is_instance(order_number)
        user_Page.confirmation_check()
        user_Page.open_loupe()
        user_Page.check_text_bonus()
        user_Page.check_bonus_confirm()
        user_Page.check_added_bonuses_count_larger_than_null()


# LGC-T2346 "Отказ" без баллов Оплата "Наличными при получении" Пользователь с бонусной картой
@allure.issue("https://jira.pochtavip.com/secure/Tests.jspa#/testCase/LGC-T2346", "LGC-T2346")
@allure.feature("Отказ")
@allure.story('Тест: "Отказ" без баллов, с картой, оплата наличными при получении')
@pytest.mark.with_card
@pytest.mark.refused
def test_refused_no_bonus_pay_cash_have_bonus_card(user_with_card, driver):

    search_item = choose_item_in_catalog.ChooseItem(user_with_card)
    search_item.get_catalog()
    search_item.get_category()
    search_item.get_list()
    search_item.get_item_card_from_product_list()
    search_item.check_available_item_sizes()
    search_item.add_item_in_cart()
    submit = order_submit.OrderSubmit(user_with_card)
    submit.open_cart()
    submit.cart_order_data()
    submit.add_item_and_order_submit()
    submit.get_order_number()
    order_number = submit.order_number

    bitrix_ops = Bitrix(driver)
    bitrix_ops.authorization()
    bitrix_ops.open(Bitrix.order_edit_link(order_number))
    bitrix_ops.change_buyout_status_to_yes()
    bitrix_ops.open(Bitrix.order_link(order_number))
    bitrix_ops.order_status_change("QI")

    login_Page = login_page.LoymaxLoginPage(driver)
    login_Page.authorization()
    call_center_page = call_center.CallCenterPage(driver)
    call_center_page.go_to_search()
    call_center_page.search_user(user_with_card.phone_number[1:])
    user_Page = user_page.UserPage(driver)
    user_Page.open_purchase_history()
    user_Page.order_number_is_instance(order_number)
    user_Page.cancellation_check()


# LGC-T2345 "Отказ" с баллами Оплата "Наличными при получении" Пользователь с бонусной картой
@allure.issue("https://jira.pochtavip.com/secure/Tests.jspa#/testCase/LGC-T2345", "LGC-T2345")
@allure.feature("Отказ")
@allure.story('Тест: "Отказ" со списанием бонусов, с картой, оплата наличными при получении')
@pytest.mark.with_card
@pytest.mark.with_bonuses
@pytest.mark.refused
def test_refused_with_bonus_pay_cash(user_with_card, driver):

    search_item = choose_item_in_catalog.ChooseItem(user_with_card)
    search_item.get_catalog()
    search_item.get_category()
    search_item.get_list()
    search_item.get_item_card_from_product_list()
    search_item.check_available_item_sizes()
    search_item.add_item_in_cart()
    submit = order_submit.OrderSubmit(user_with_card)
    submit.open_cart()
    submit.cart_order_data()
    submit.use_bonuses()
    submit.add_item_and_order_submit()
    submit.get_order_number()
    pay_bonuses = order_submit.WriteOff(submit.order_submit_response, submit.bonuses, user_with_card.user_card)
    pay_bonuses.send_bonuses()
    order_number = submit.order_number

    bitrix_ops = Bitrix(driver)
    bitrix_ops.authorization()
    bitrix_ops.open(Bitrix.order_edit_link(order_number))
    bitrix_ops.change_buyout_status_to_yes()
    bitrix_ops.open(Bitrix.order_link(order_number))
    bitrix_ops.order_status_change("QI")

    login_Page = login_page.LoymaxLoginPage(driver)
    login_Page.authorization()
    call_center_page = call_center.CallCenterPage(driver)
    call_center_page.go_to_search()
    call_center_page.search_user(user_with_card.phone_number[1:])
    user_Page = user_page.UserPage(driver)
    user_Page.open_purchase_history()
    user_Page.order_number_is_instance(order_number)
    user_Page.cancellation_check()


# LGC-T2344 "Отмена" без баллов Оплата "Наличными при получении" Пользователь с бонусной картой
@allure.issue("https://jira.pochtavip.com/secure/Tests.jspa#/testCase/LGC-T2344", "LGC-T2344")
@allure.feature("Отмена")
@allure.story('Тест: "Отмена" без баллов, с картой, оплата наличными при получении')
@pytest.mark.with_card
@pytest.mark.cancelled
def test_cancelled_no_bonus_pay_cash(user_with_card, driver):
    search_item = choose_item_in_catalog.ChooseItem(user_with_card)
    search_item.get_catalog()
    search_item.get_category()
    search_item.get_list()
    search_item.get_item_card_from_product_list()
    search_item.check_available_item_sizes()
    search_item.add_item_in_cart()
    submit = order_submit.OrderSubmit(user_with_card)
    submit.open_cart()
    submit.cart_order_data()
    submit.add_item_and_order_submit()
    submit.get_order_number()
    order_number = submit.order_number

    bitrix_ops = Bitrix(driver)
    bitrix_ops.authorization()
    bitrix_ops.open(Bitrix.order_link(order_number))
    bitrix_ops.order_status_change("MB")

    login_Page = login_page.LoymaxLoginPage(driver)
    login_Page.authorization()
    call_center_page = call_center.CallCenterPage(driver)
    call_center_page.go_to_search()
    call_center_page.search_user(user_with_card.phone_number[1:])
    user_Page = user_page.UserPage(driver)
    user_Page.open_purchase_history()
    user_Page.order_number_is_instance(order_number)
    user_Page.cancellation_check()


# LGC-T2335 "Отмена" с баллами Оплата "Наличными при получении" Пользователь с бонусной картой
@allure.issue("https://jira.pochtavip.com/secure/Tests.jspa#/testCase/LGC-T2335", "LGC-T2335")
@allure.feature("Отмена")
@allure.story('Тест: "Отмена" со списанием бонусов, с картой, оплата наличными при получении')
@pytest.mark.with_card
@pytest.mark.with_bonuses
@pytest.mark.cancelled
def test_cancelled_with_bonus_pay_cash(user_with_card, driver):
    search_item = choose_item_in_catalog.ChooseItem(user_with_card)
    search_item.get_catalog()
    search_item.get_category()
    search_item.get_list()
    search_item.get_item_card_from_product_list()
    search_item.check_available_item_sizes()
    search_item.add_item_in_cart()
    submit = order_submit.OrderSubmit(user_with_card)
    submit.open_cart()
    submit.cart_order_data()
    submit.use_bonuses()
    submit.add_item_and_order_submit()
    submit.get_order_number()
    pay_bonuses = order_submit.WriteOff(submit.order_submit_response, submit.bonuses, user_with_card.user_card)
    pay_bonuses.send_bonuses()
    order_number = submit.order_number

    bitrix_ops = Bitrix(driver)
    bitrix_ops.authorization()
    bitrix_ops.open(Bitrix.order_link(order_number))
    bitrix_ops.order_status_change("MB")

    login_Page = login_page.LoymaxLoginPage(driver)
    login_Page.authorization()
    call_center_page = call_center.CallCenterPage(driver)
    call_center_page.go_to_search()
    call_center_page.search_user(user_with_card.phone_number[1:])
    user_Page = user_page.UserPage(driver)
    user_Page.open_purchase_history()
    user_Page.order_number_is_instance(order_number)
    user_Page.cancellation_check()


# LGC-T2347 "Оформлен" Оплата "Наличными при получении" Пользователь без бонусной карты
@allure.issue("https://jira.pochtavip.com/secure/Tests.jspa#/testCase/LGC-T2347", "LGC-T2347")
@allure.feature("Оформлен")
@allure.story('Тест: "Оформлен" без бонусной карты, оплата наличными при получении')
@pytest.mark.no_card
@pytest.mark.processed
def test_processed_pay_cash_no_bonus_card(user_no_card, driver): # в черновом варианте - просто оформление заказа
    search_item = choose_item_in_catalog.ChooseItem(user_no_card)
    search_item.get_catalog()
    search_item.get_category()
    search_item.get_list()
    search_item.get_item_card_from_product_list()
    search_item.check_available_item_sizes()
    search_item.add_item_in_cart()
    submit = order_submit.OrderSubmit(user_no_card)
    submit.open_cart()
    submit.cart_order_data()
    submit.add_item_and_order_submit()
    submit.get_order_number()
    order_number = submit.order_number
    bitrix_ops = Bitrix(driver)
    bitrix_ops.authorization()
    bitrix_ops.open(Bitrix.order_link(order_number))
    bitrix_ops.order_status_change("AB")


# LGC-T2341 "Оформлен"без баллов Оплата "Наличными при получении" Пользователь с бонусной картой
@allure.issue("https://jira.pochtavip.com/secure/Tests.jspa#/testCase/LGC-T2341", "LGC-T2341")
@allure.feature("Оформлен")
@allure.story('Тест: "Оформлен" без баллов, с картой, оплата наличными при получении')
@pytest.mark.with_card
@pytest.mark.processed
def test_processed_pay_cash_with_bonus_card(user_with_card, driver): # в черновом варианте - просто оформление заказа

    search_item = choose_item_in_catalog.ChooseItem(user_with_card)
    search_item.get_catalog()
    search_item.get_category()
    search_item.get_list()
    search_item.get_item_card_from_product_list()
    search_item.check_available_item_sizes()
    search_item.add_item_in_cart()
    submit = order_submit.OrderSubmit(user_with_card)
    submit.open_cart()
    submit.cart_order_data()
    submit.add_item_and_order_submit()
    submit.get_order_number()
    order_number = submit.order_number
    bitrix_ops = Bitrix(driver)
    bitrix_ops.authorization()
    bitrix_ops.open(Bitrix.order_link(order_number))
    bitrix_ops.order_status_change("AB")

    login_Page = login_page.LoymaxLoginPage(driver)
    login_Page.authorization()
    call_center_page = call_center.CallCenterPage(driver)

    # call_center_page.go_to_search()
    # call_center_page.search_user()
    # user_Page = user_page.UserPage(driver)
    # user_Page.open_purchase_history()
    # user_Page.order_number_is_instance(order_number)
    # user_Page.creation_check()


# LGC-T2342 "Оформлен" с баллами Оплата "Наличными при получении" Пользователь с бонусной картой
@allure.issue("https://jira.pochtavip.com/secure/Tests.jspa#/testCase/LGC-T2342", "LGC-T2342")
@allure.feature("Оформлен")
@allure.story('Тест: "Оформлен" со списанием бонусов, с картой, оплата наличными при получении')
@pytest.mark.with_card
@pytest.mark.with_bonuses
@pytest.mark.processed
def test_processed_with_bonus_pay_cash(user_with_card, driver):
    search_item = choose_item_in_catalog.ChooseItem(user_with_card)
    search_item.get_catalog()
    search_item.get_category()
    search_item.get_list()
    search_item.get_item_card_from_product_list()
    search_item.check_available_item_sizes()
    search_item.add_item_in_cart()
    submit = order_submit.OrderSubmit(user_with_card)
    submit.open_cart()
    submit.cart_order_data()
    submit.use_bonuses()
    submit.add_item_and_order_submit()
    submit.get_order_number()
    pay_bonuses = order_submit.WriteOff(submit.order_submit_response, submit.bonuses, user_with_card.user_card)
    pay_bonuses.send_bonuses()
    order_number = submit.order_number

    bitrix_ops = Bitrix(driver)
    bitrix_ops.authorization()
    bitrix_ops.open(Bitrix.order_link(order_number))
    bitrix_ops.order_status_change("AB")
    bitrix_ops.open(Bitrix.order_edit_link(order_number))
    bitrix_ops.change_buyout_status_to_yes()

    login_Page = login_page.LoymaxLoginPage(driver)
    login_Page.authorization()
    call_center_page = call_center.CallCenterPage(driver)

    call_center_page.go_to_search()
    call_center_page.search_user(user_with_card.phone_number[1:])
    user_Page = user_page.UserPage(driver)
    user_Page.open_purchase_history()
    user_Page.order_number_is_instance(order_number)
    user_Page.creation_check()


# LGC-T2334 "Частичный отказ" без баллов Оплата "Наличными при получении" в корзине 2 товара Пользователь без бонусной карты
@allure.issue("https://jira.pochtavip.com/secure/Tests.jspa#/testCase/LGC-T2334", "LGC-T2334")
@allure.feature("Частичный отказ")
@allure.story('Тест: "Частичный отказ" без бонусной карты, оплата наличными при получении')
@pytest.mark.no_card
@pytest.mark.partial_cancelled
def test_partial_cancelled_pay_cash_no_bonus_card(user_no_card, driver):
    search_item = choose_item_in_catalog.ChooseItem(user_no_card)
    search_item.get_catalog()
    search_item.get_category()
    search_item.get_list()
    search_item.get_item_card_from_product_list()
    search_item.check_available_item_sizes()
    search_item.add_item_in_cart()
    search_item.get_catalog()
    search_item.get_category()
    search_item.get_list()
    search_item.get_item_card_from_product_list()
    search_item.check_available_item_sizes()
    search_item.add_item_in_cart()
    submit = order_submit.OrderSubmit(user_no_card)
    submit.open_cart()
    submit.cart_order_data()
    submit.add_item_and_order_submit()
    submit.get_order_number()
    order_number = submit.order_number

    bitrix_ops = Bitrix(driver)
    bitrix_ops.authorization()
    bitrix_ops.open(Bitrix.order_edit_link(order_number))
    bitrix_ops.change_buyout_status_to_yes()
    bitrix_ops.open(Bitrix.order_link(order_number))
    bitrix_ops.order_status_change("OI")


# LGC-T2339 "Частичный отказ" без баллов Оплата "Наличными при получении" в корзине 2 товара Пользователь с бонусной картой
@allure.issue("https://jira.pochtavip.com/secure/Tests.jspa#/testCase/LGC-T2339", "LGC-T2339")
@allure.feature("Частичный отказ")
@allure.story('Тест: "Частичный отказ" без баллов, с картой, оплата наличными при получении')
@pytest.mark.with_card
@pytest.mark.partial_cancelled
def test_partial_cancelled_no_bonus_pay_cash_with_bonus_card(user_with_card, driver):

    search_item = choose_item_in_catalog.ChooseItem(user_with_card)
    search_item.get_catalog()
    search_item.get_category()
    search_item.get_list()
    search_item.get_item_card_from_product_list()
    search_item.check_available_item_sizes()
    search_item.add_item_in_cart()
    search_item.get_catalog()
    search_item.get_category()
    search_item.get_list()
    search_item.get_item_card_from_product_list()
    search_item.check_available_item_sizes()
    search_item.add_item_in_cart()
    submit = order_submit.OrderSubmit(user_with_card)
    submit.open_cart()
    submit.cart_order_data()
    submit.add_item_and_order_submit()
    submit.get_order_number()
    order_number = submit.order_number

    bitrix_ops = Bitrix(driver)
    bitrix_ops.authorization()
    bitrix_ops.open(Bitrix.order_edit_link(order_number))
    bitrix_ops.change_buyout_status_to_yes()
    time.sleep(60)
    bitrix_ops.open(Bitrix.order_link(order_number))
    bitrix_ops.order_status_change("OI")

    login_Page = login_page.LoymaxLoginPage(driver)
    login_Page.authorization()
    call_center_page = call_center.CallCenterPage(driver)
    call_center_page.go_to_search()
    call_center_page.search_user(user_with_card.phone_number[1:])
    user_Page = user_page.UserPage(driver)
    user_Page.open_purchase_history()
    user_Page.order_number_is_instance(order_number)
    user_Page.partial_cancel_two_statuses_check()
    user_Page.confirmation_check()
    user_Page.partial_cancel_cancellation_check()
    user_Page.open_loupe()
    user_Page.check_text_bonus()
    user_Page.check_bonus_confirm()
    user_Page.check_added_bonuses_count_larger_than_null()


# LGC-T2340 "Частичный отказ" с баллами Оплата "Наличными при получении" в корзине 2 товара Пользователь с бонусной картой
@allure.issue("https://jira.pochtavip.com/secure/Tests.jspa#/testCase/LGC-T2340", "LGC-T2340")
@allure.feature("Частичный отказ")
@allure.story('Тест: "Частичный отказ" со списанием бонусов, с картой, оплата наличными при получении')
@pytest.mark.with_card

@pytest.mark.partial_cancelled
def test_partial_cancelled_with_bonus_pay_cash(user_with_card, driver):

    search_item = choose_item_in_catalog.ChooseItem(user_with_card)
    search_item.get_catalog()
    search_item.get_category()
    search_item.get_list()
    search_item.get_item_card_from_product_list()
    search_item.check_available_item_sizes()
    search_item.add_item_in_cart()
    search_item.get_catalog()
    search_item.get_category()
    search_item.get_list()
    search_item.get_item_card_from_product_list()
    search_item.check_available_item_sizes()
    search_item.add_item_in_cart()
    submit = order_submit.OrderSubmit(user_with_card)
    submit.open_cart()
    submit.cart_order_data()
    submit.use_bonuses()
    submit.add_item_and_order_submit()
    submit.get_order_number()
    pay_bonuses = order_submit.WriteOff(submit.order_submit_response, submit.bonuses, user_with_card.user_card)
    pay_bonuses.send_bonuses()
    order_number = submit.order_number

    bitrix_ops = Bitrix(driver)
    bitrix_ops.authorization()
    bitrix_ops.open(Bitrix.order_edit_link(order_number))
    bitrix_ops.change_buyout_status_to_yes()
    time.sleep(60)
    bitrix_ops.open(Bitrix.order_link(order_number))
    bitrix_ops.order_status_change("OI")

    login_Page = login_page.LoymaxLoginPage(driver)
    login_Page.authorization()
    call_center_page = call_center.CallCenterPage(driver)
    call_center_page.go_to_search()
    call_center_page.search_user(user_with_card.phone_number[1:])
    user_Page = user_page.UserPage(driver)
    user_Page.open_purchase_history()
    user_Page.order_number_is_instance(order_number)
    user_Page.partial_cancel_two_statuses_check()
    user_Page.confirmation_check()
    user_Page.partial_cancel_cancellation_check()
    user_Page.open_loupe()
    user_Page.check_text_bonus()
    user_Page.check_bonus_confirm()
    user_Page.check_added_bonuses_count_larger_than_null()





