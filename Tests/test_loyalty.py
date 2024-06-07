import pytest

from API import authorization, choose_item_in_catalog, order_submit
from Bitrix import bitrix
from Loymax import login_page, user_page, call_center

def test_delivered_no_bonus_pay_cash_no_bonus_card(user_no_card): # LGC-T2332 "Доставлен" без баллов Оплата "Наличными при получении" Пользователь без бонусной карты
    print("")
    # Шаг 1: Заходим в приложение
    # Шаг 2: Вводим номер
    # Шаг 3: Вводим код
    search_item = choose_item_in_catalog.ChooseItem(user_no_card)
    search_item.get_catalog()# Шаг 4: GET /catalog
    # !!! Шаг 5: Тапнуть на любую категорию одежды GET/catalog/{categoryUri}
    # !!! Шаг 6: Тапнуть на любой вид одежды GET/category/{categoryUri}/list
    search_item.get_products_list_sorted_by_gender() # Шаг 5-6*: GET /catalog/{gender}
    search_item.get_item_card_from_product_list() # Шаг 7: В ленте товаров тапом открыть карточку любого товара стоимостью больше 2 000 р.GET/v2/product/{productId}
    search_item.check_available_item_sizes()# Шаг 8.1: Выбираем размер
    search_item.add_item_in_cart() # Шаг 8.2: Тап по кнопке "В корзину"
    submit = order_submit.OrderSubmit(user_no_card)
    submit.open_cart()# Шаг 9: Тап по кнопке "Корзина" в нижнем правом углу. Переходим в корзину GET/cart
    submit.cart_order_data() # Шаг 10: Тап по кнопке "Оформить заказ" в нижней части экрана (оформляем заказ) GET/cart/order
    # !!! Шаг 11: Вводим ФИО и номер и почту. Заполняем данные оформления заказа покупателя. POST/order/customer
    # !!! Шаг 12: Заполнить Город доставки POST/city
    # !!! Шаг 13: Выбрать способ доставки и указать адрес или ПВЗ.Заполняем данные оформления заказа "Доставка". POST/order/delivery GET/city/address/search POST/order/address
    # !!! Шаг 14: Выбрать службу доставки и актуальный слот доставки POST/order/address
    # !!! Шаг 15: Тап на оформление заказа GET/cart/order
    # !!! Шаг 16: Выбираем оплату Наличными при получении POST/order/payment
    submit.add_item_and_order_submit() # Шаг 17: тап по кнопке "Оформить заказ" POST/order/submit
    order_number = order_submit.get_order_number()
    # Шаг 17: Перейти в битрикс администрирование