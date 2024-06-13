import pytest
from API import choose_item_in_catalog, order_submit
from Bitrix.bitrix import Bitrix
from Loymax import login_page, user_page, call_center
import time

# LGC-T2332 "Доставлен" без баллов Оплата "Наличными при получении" Пользователь без бонусной карты
def test_delivered_no_bonus_pay_cash_no_bonus_card(user_no_card, browser):
    #                                                                     # Шаг 1: Заходим в приложение
    #                                                                     # Шаг 2: Вводим номер
    #                                                                     # Шаг 3: Вводим код
    search_item = choose_item_in_catalog.ChooseItem(user_no_card)
    search_item.get_catalog()                                           # Шаг 4: GET /catalog
    #                                                                     # !!! Шаг 5: Тапнуть на любую категорию одежды GET/catalog/{categoryUri}
    #                                                                     # !!! Шаг 6: Тапнуть на любой вид одежды GET/category/{categoryUri}/list
    search_item.get_products_list_sorted_by_gender()                    # Шаг 5-6*: GET /catalog/{gender}
    search_item.get_item_card_from_product_list()                       # Шаг 7: В ленте товаров тапом открыть карточку любого товара стоимостью больше 2 000 р.GET/v2/product/{productId}
    search_item.check_available_item_sizes()                            # Шаг 8.1: Выбираем размер
    search_item.add_item_in_cart()                                      # Шаг 8.2: Тап по кнопке "В корзину"
    submit = order_submit.OrderSubmit(user_no_card)
    submit.open_cart()                                                  # Шаг 9: Тап по кнопке "Корзина" в нижнем правом углу. Переходим в корзину GET/cart
    submit.cart_order_data()                                            # Шаг 10: Тап по кнопке "Оформить заказ" в нижней части экрана (оформляем заказ) GET/cart/order
    #                                                                     # !!! Шаг 11: Вводим ФИО и номер и почту. Заполняем данные оформления заказа покупателя. POST/order/customer
    #                                                                     # !!! Шаг 12: Заполнить Город доставки POST/city
    #                                                                     # !!! Шаг 13: Выбрать способ доставки и указать адрес или ПВЗ.Заполняем данные оформления заказа "Доставка". POST/order/delivery GET/city/address/search POST/order/address
    #                                                                     # !!! Шаг 14: Выбрать службу доставки и актуальный слот доставки POST/order/address
    #                                                                     # !!! Шаг 15: Тап на оформление заказа GET/cart/order
    #                                                                     # !!! Шаг 16: Выбираем оплату Наличными при получении POST/order/payment
    submit.add_item_and_order_submit()                                  # Шаг 17: тап по кнопке "Оформить заказ" POST/order/submit
    submit.get_order_number()
    order_number = submit.order_number
    bitrix_ops = Bitrix(browser)# Шаг 18: Перейти в битрикс администрирование
    bitrix_ops.authorization()
    bitrix_ops.open(Bitrix.order_edit_link(order_number))
    bitrix_ops.change_buyout_status_to_yes()
    bitrix_ops.open(Bitrix.order_link(order_number))
    bitrix_ops.order_status_change("NI")


# LGC-T2337 "Доставлен" без баллов Оплата "Наличными при получении" Пользователь с бонусной картой
def test_delivered_no_bonus_pay_cash_have_bonus_card(user_with_card, browser):

    search_item = choose_item_in_catalog.ChooseItem(user_with_card)
    search_item.get_catalog()
    search_item.get_products_list_sorted_by_gender()
    search_item.get_item_card_from_product_list()
    search_item.check_available_item_sizes()
    search_item.add_item_in_cart()
    submit = order_submit.OrderSubmit(user_with_card)
    submit.open_cart()
    submit.cart_order_data()
    submit.add_item_and_order_submit()
    submit.get_order_number()
    order_number = submit.order_number

    bitrix_ops = Bitrix(browser)
    bitrix_ops.authorization()
    bitrix_ops.open(Bitrix.order_edit_link(order_number))
    bitrix_ops.change_buyout_status_to_yes()
    bitrix_ops.open(Bitrix.order_link(order_number))
    bitrix_ops.order_status_change("NI")

    login_Page = login_page.LoymaxLoginPage(browser)
    login_Page.authorization()
    call_center_page = call_center.CallCenterPage(browser)
    call_center_page.go_to_search()
    call_center_page.search_user()
    user_Page = user_page.UserPage(browser)
    user_Page.open_purchase_history()
    user_Page.order_number_is_instance(order_number)
    user_Page.confirmation_check()
    user_Page.open_loupe()
    user_Page.check_text_bonus()
    user_Page.check_bonus_confirm()
    user_Page.check_added_bonuses_count_larger_than_null()


# LGC-T2348 Доставлен" с баллами Оплата "Наличными при получении" Пользователь с бонусной картой
def test_delivered_with_bonus_pay_cash(user_with_card, browser):

    search_item = choose_item_in_catalog.ChooseItem(user_with_card)
    search_item.get_catalog()
    search_item.get_products_list_sorted_by_gender()
    search_item.get_item_card_from_product_list()
    search_item.check_available_item_sizes()
    search_item.add_item_in_cart()
    submit = order_submit.OrderSubmit(user_with_card)
    submit.open_cart()
    submit.cart_order_data()
    submit.add_item_and_order_submit()
    submit.get_order_number()
    pay_bonuses = order_submit.WriteOff(submit.order_submit_response, user_with_card.user_card)
    pay_bonuses.send_bonuses()
    order_number = submit.order_number

    bitrix_ops = Bitrix(browser)
    bitrix_ops.authorization()
    bitrix_ops.open(Bitrix.order_edit_link(order_number))
    bitrix_ops.change_buyout_status_to_yes()
    bitrix_ops.open(Bitrix.order_link(order_number))
    bitrix_ops.order_status_change("NI")

    login_Page = login_page.LoymaxLoginPage(browser)
    login_Page.authorization()
    call_center_page = call_center.CallCenterPage(browser)

    call_center_page.go_to_search()
    call_center_page.search_user()
    user_Page = user_page.UserPage(browser)
    user_Page.open_purchase_history()
    user_Page.order_number_is_instance(order_number)
    user_Page.confirmation_check()
    user_Page.open_loupe()
    user_Page.check_text_bonus()
    user_Page.check_bonus_confirm()
    user_Page.check_added_bonuses_count_larger_than_null()


# LGC-T2346 "Отказ" без баллов Оплата "Наличными при получении" Пользователь с бонусной картой
def test_refused_no_bonus_pay_cash_have_bonus_card(user_with_card, browser):

    search_item = choose_item_in_catalog.ChooseItem(user_with_card)
    search_item.get_catalog()
    search_item.get_products_list_sorted_by_gender()
    search_item.get_item_card_from_product_list()
    search_item.check_available_item_sizes()
    search_item.add_item_in_cart()
    submit = order_submit.OrderSubmit(user_with_card)
    submit.open_cart()
    submit.cart_order_data()
    submit.add_item_and_order_submit()
    submit.get_order_number()
    order_number = submit.order_number

    bitrix_ops = Bitrix(browser)
    bitrix_ops.authorization()
    bitrix_ops.open(Bitrix.order_edit_link(order_number))
    bitrix_ops.change_buyout_status_to_yes()
    bitrix_ops.open(Bitrix.order_link(order_number))
    bitrix_ops.order_status_change("QI")

    login_Page = login_page.LoymaxLoginPage(browser)
    login_Page.authorization()
    call_center_page = call_center.CallCenterPage(browser)

    call_center_page.go_to_search()
    call_center_page.search_user()
    user_Page = user_page.UserPage(browser)
    user_Page.open_purchase_history()
    user_Page.order_number_is_instance(order_number)
    user_Page.cancellation_check()


# LGC-T2345 "Отказ" с баллами Оплата "Наличными при получении" Пользователь с бонусной картой
def test_refused_with_bonus_pay_cash(user_with_card, browser):

    search_item = choose_item_in_catalog.ChooseItem(user_with_card)
    search_item.get_catalog()
    search_item.get_products_list_sorted_by_gender()
    search_item.get_item_card_from_product_list()
    search_item.check_available_item_sizes()
    search_item.add_item_in_cart()
    submit = order_submit.OrderSubmit(user_with_card)
    submit.open_cart()
    submit.cart_order_data()
    submit.add_item_and_order_submit()
    submit.get_order_number()
    pay_bonuses = order_submit.WriteOff(submit.order_submit_response, user_with_card.user_card)
    pay_bonuses.send_bonuses()
    order_number = submit.order_number

    bitrix_ops = Bitrix(browser)
    bitrix_ops.authorization()
    bitrix_ops.open(Bitrix.order_edit_link(order_number))
    bitrix_ops.change_buyout_status_to_yes()
    bitrix_ops.open(Bitrix.order_link(order_number))
    bitrix_ops.order_status_change("QI")

    login_Page = login_page.LoymaxLoginPage(browser)
    login_Page.authorization()
    call_center_page = call_center.CallCenterPage(browser)

    call_center_page.go_to_search()
    call_center_page.search_user()
    user_Page = user_page.UserPage(browser)
    user_Page.open_purchase_history()
    user_Page.order_number_is_instance(order_number)
    user_Page.cancellation_check()


# LGC-T2344 "Отмена" без баллов Оплата "Наличными при получении" Пользователь с бонусной картой
def test_cancelled_no_bonus_pay_cash(user_with_card, browser):
    search_item = choose_item_in_catalog.ChooseItem(user_with_card)
    search_item.get_catalog()
    search_item.get_products_list_sorted_by_gender()
    search_item.get_item_card_from_product_list()
    search_item.check_available_item_sizes()
    search_item.add_item_in_cart()
    submit = order_submit.OrderSubmit(user_with_card)
    submit.open_cart()
    submit.cart_order_data()
    submit.add_item_and_order_submit()
    submit.get_order_number()
    order_number = submit.order_number

    bitrix_ops = Bitrix(browser)
    bitrix_ops.authorization()
    bitrix_ops.open(Bitrix.order_link(order_number))
    bitrix_ops.order_status_change("MB")

    login_Page = login_page.LoymaxLoginPage(browser)
    login_Page.authorization()
    call_center_page = call_center.CallCenterPage(browser)

    call_center_page.go_to_search()
    call_center_page.search_user()
    user_Page = user_page.UserPage(browser)
    user_Page.open_purchase_history()
    user_Page.order_number_is_instance(order_number)
    user_Page.cancellation_check()


# LGC-T2335 "Отмена" с баллами Оплата "Наличными при получении" Пользователь с бонусной картой
def test_cancelled_with_bonus_pay_cash(user_with_card, browser):
    search_item = choose_item_in_catalog.ChooseItem(user_with_card)
    search_item.get_catalog()
    search_item.get_products_list_sorted_by_gender()
    search_item.get_item_card_from_product_list()
    search_item.check_available_item_sizes()
    search_item.add_item_in_cart()
    submit = order_submit.OrderSubmit(user_with_card)
    submit.open_cart()
    submit.cart_order_data()
    submit.add_item_and_order_submit()
    submit.get_order_number()
    order_number = submit.order_number
    pay_bonuses = order_submit.WriteOff(submit.order_submit_response, user_with_card.user_card)
    pay_bonuses.send_bonuses()

    bitrix_ops = Bitrix(browser)
    bitrix_ops.authorization()
    bitrix_ops.open(Bitrix.order_link(order_number))
    bitrix_ops.order_status_change("MB")

    login_Page = login_page.LoymaxLoginPage(browser)
    login_Page.authorization()
    call_center_page = call_center.CallCenterPage(browser)

    call_center_page.go_to_search()
    call_center_page.search_user()
    user_Page = user_page.UserPage(browser)
    user_Page.open_purchase_history()
    user_Page.order_number_is_instance(order_number)
    user_Page.cancellation_check()


# LGC-T2347 "Оформлен" Оплата "Наличными при получении" Пользователь без бонусной карты
def test_processed_pay_cash_no_bonus_card(user_no_card): # в черновом варианте - просто оформление заказа
    search_item = choose_item_in_catalog.ChooseItem(user_no_card)
    search_item.get_catalog()
    search_item.get_products_list_sorted_by_gender()
    search_item.get_item_card_from_product_list()
    search_item.check_available_item_sizes()
    search_item.add_item_in_cart()
    submit = order_submit.OrderSubmit(user_no_card)
    submit.open_cart()
    submit.cart_order_data()
    submit.add_item_and_order_submit()
    submit.get_order_number()


# LGC-T2341 "Оформлен" Оплата "Наличными при получении" Пользователь с бонусной картой

def test_processed_pay_cash_with_bonus_card(user_with_card): # в черновом варианте - просто оформление заказа
    search_item = choose_item_in_catalog.ChooseItem(user_with_card)
    search_item.get_catalog()
    search_item.get_products_list_sorted_by_gender()
    search_item.get_item_card_from_product_list()
    search_item.check_available_item_sizes()
    search_item.add_item_in_cart()
    submit = order_submit.OrderSubmit(user_with_card)
    submit.open_cart()
    submit.cart_order_data()
    submit.add_item_and_order_submit()
    submit.get_order_number()


# LGC-T2342 "Оформлен" с баллами Оплата "Наличными при получении" Пользователь с бонусной картой
def test_processed_with_bonus_pay_cash(user_with_card, browser):
    search_item = choose_item_in_catalog.ChooseItem(user_with_card)
    search_item.get_catalog()
    search_item.get_products_list_sorted_by_gender()
    search_item.get_item_card_from_product_list()
    search_item.check_available_item_sizes()
    search_item.add_item_in_cart()
    submit = order_submit.OrderSubmit(user_with_card)
    submit.open_cart()
    submit.cart_order_data()
    submit.add_item_and_order_submit()
    submit.get_order_number()
    pay_bonuses = order_submit.WriteOff(submit.order_submit_response, user_with_card.user_card)
    pay_bonuses.send_bonuses()
    order_number = submit.order_number

    bitrix_ops = Bitrix(browser)
    bitrix_ops.authorization()
    bitrix_ops.open(Bitrix.order_edit_link(order_number))
    bitrix_ops.change_buyout_status_to_yes()

    login_Page = login_page.LoymaxLoginPage(browser)
    login_Page.authorization()
    call_center_page = call_center.CallCenterPage(browser)

    call_center_page.go_to_search()
    call_center_page.search_user()
    user_Page = user_page.UserPage(browser)
    user_Page.open_purchase_history()
    user_Page.order_number_is_instance(order_number)
    user_Page.creation_check()


# LGC-T2334 "Частичный отказ" без баллов Оплата "Наличными при получении" в корзине 2 товара Пользователь без бонусной карты
@pytest.mark.partial_cancelled
def test_partial_cancelled_pay_cash_no_bonus_card(user_no_card, browser):
    search_item = choose_item_in_catalog.ChooseItem(user_no_card)
    search_item.get_catalog()
    search_item.get_products_list_sorted_by_gender()
    search_item.get_item_card_from_product_list()
    search_item.check_available_item_sizes()
    search_item.add_item_in_cart()
    search_item.get_catalog()
    search_item.get_products_list_sorted_by_gender()
    search_item.get_item_card_from_product_list()
    search_item.check_available_item_sizes()
    search_item.add_item_in_cart()
    submit = order_submit.OrderSubmit(user_no_card)
    submit.open_cart()
    submit.cart_order_data()
    submit.add_item_and_order_submit()
    submit.get_order_number()
    order_number = submit.order_number

    bitrix_ops = Bitrix(browser)
    bitrix_ops.authorization()
    bitrix_ops.open(Bitrix.order_edit_link(order_number))
    bitrix_ops.change_buyout_status_to_yes()
    bitrix_ops.open(Bitrix.order_link(order_number))
    bitrix_ops.order_status_change("OI")


# LGC-T2339 "Частичный отказ" без баллов Оплата "Наличными при получении" в корзине 2 товара Пользователь с бонусной картой
@pytest.mark.partial_cancelled
def test_partial_cancelled_no_bonus_pay_cash_with_bonus_card(user_with_card, browser):

    search_item = choose_item_in_catalog.ChooseItem(user_with_card)
    search_item.get_catalog()
    search_item.get_products_list_sorted_by_gender()
    search_item.get_item_card_from_product_list()
    search_item.check_available_item_sizes()
    search_item.add_item_in_cart()
    search_item.get_catalog()
    search_item.get_products_list_sorted_by_gender()
    search_item.get_item_card_from_product_list()
    search_item.check_available_item_sizes()
    search_item.add_item_in_cart()
    submit = order_submit.OrderSubmit(user_with_card)
    submit.open_cart()
    submit.cart_order_data()
    submit.add_item_and_order_submit()
    submit.get_order_number()
    order_number = submit.order_number

    bitrix_ops = Bitrix(browser)
    bitrix_ops.authorization()
    bitrix_ops.open(Bitrix.order_edit_link(order_number))
    bitrix_ops.change_buyout_status_to_yes()
    time.sleep(60)
    bitrix_ops.open(Bitrix.order_link(order_number))
    bitrix_ops.order_status_change("OI")

    login_Page = login_page.LoymaxLoginPage(browser)
    login_Page.authorization()
    call_center_page = call_center.CallCenterPage(browser)
    call_center_page.go_to_search()
    call_center_page.search_user()
    user_Page = user_page.UserPage(browser)
    user_Page.open_purchase_history()
    user_Page.order_number_is_instance(order_number)
    user_Page.partial_cancel_two_statuses_check()
    user_Page.confirmation_check()
    user_Page.partial_cancel_cancellation_check()


# LGC-T2340 "Частичный отказ" с баллами Оплата "Наличными при получении" в корзине 2 товара Пользователь с бонусной картой
@pytest.mark.partial_cancelled
def test_partial_cancelled_with_bonus_pay_cash(user_with_card, browser):

    search_item = choose_item_in_catalog.ChooseItem(user_with_card)
    search_item.get_catalog()
    search_item.get_products_list_sorted_by_gender()
    search_item.get_item_card_from_product_list()
    search_item.check_available_item_sizes()
    search_item.add_item_in_cart()
    search_item.get_catalog()
    search_item.get_products_list_sorted_by_gender()
    search_item.get_item_card_from_product_list()
    search_item.check_available_item_sizes()
    search_item.add_item_in_cart()
    submit = order_submit.OrderSubmit(user_with_card)
    submit.open_cart()
    submit.cart_order_data()
    submit.add_item_and_order_submit()
    submit.get_order_number()
    pay_bonuses = order_submit.WriteOff(submit.order_submit_response, user_with_card.user_card)
    pay_bonuses.send_bonuses()
    order_number = submit.order_number

    bitrix_ops = Bitrix(browser)
    bitrix_ops.authorization()
    bitrix_ops.open(Bitrix.order_edit_link(order_number))
    bitrix_ops.change_buyout_status_to_yes()
    time.sleep(60)
    bitrix_ops.open(Bitrix.order_link(order_number))
    bitrix_ops.order_status_change("OI")

    login_Page = login_page.LoymaxLoginPage(browser)
    login_Page.authorization()
    call_center_page = call_center.CallCenterPage(browser)
    call_center_page.go_to_search()
    call_center_page.search_user()
    user_Page = user_page.UserPage(browser)
    user_Page.open_purchase_history()
    user_Page.order_number_is_instance(order_number)
    user_Page.partial_cancel_two_statuses_check()
    user_Page.confirmation_check()
    user_Page.partial_cancel_cancellation_check()





