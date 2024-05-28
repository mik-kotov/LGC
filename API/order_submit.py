from API import locators_api
from random import randint
from API import data
import json
from API import authorization
from API import choose_item_in_catalog

api_client = authorization.api_client
def open_cart():
    print('Открываем корзину')
    get_cart = api_client.get(locators_api.URL_API_SERVICE + locators_api.CART)
    print(get_cart.json())
    return get_cart
def cart_order_data():
    print('Просматриваем данные заказа для корзины')
    cart_data = api_client.get(locators_api.URL_API_SERVICE + locators_api.CART_ORDER)
    print(cart_data.json())
    return cart_data
def use_bonuses():
    card_number = data.user_card
    bonuses_to_spend = randint(1,20)
    body_for_use_bonuses = {"bonus_card": f"{card_number}", "bonuses_spend_count": bonuses_to_spend}
    post_bonuses = api_client.post(locators_api.URL_API_SERVICE + locators_api.ORDER_SUBMIT,
                                   data=json.dumps(body_for_use_bonuses))
    print("Применены бонусы")
    print(f"Списано баллов: {bonuses_to_spend}")
    return post_bonuses
def add_item_and_order_submit():
    body_for_order_submit = {'need_bonus_card_issue': True}
    order_submit = api_client.post(locators_api.URL_API_SERVICE + locators_api.ORDER_SUBMIT,
                                   data=json.dumps(body_for_order_submit))
    print(order_submit.json())
    get_order_number = order_submit.json()['response']['id']
    print("Заказ оформлен")
    print(f"Номер заказа: {get_order_number}")
    return get_order_number





