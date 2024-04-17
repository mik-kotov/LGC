import random
from API import configuration
import requests
from API import data
import json
from API import authorization
from API import choose_item_in_catalog

def open_cart():
    print('Открываем корзину')
    get_cart = requests.get(configuration.URL_API_SERVICE + configuration.CART,
                            headers=authorization.headers_with_user_auth_token)
    return get_cart
def cart_order_data():
    open_cart()
    print('Просматриваем данные заказа для корзины')
    get_cart = requests.get(configuration.URL_API_SERVICE + configuration.CART,
                            headers=authorization.headers_with_user_auth_token)
    return
    print(open_cart().json())

def add_item_and_order_submit():
    choose_item_in_catalog.add_item_in_cart()
    body_for_order_submit = {'need_bonus_card_issue': True }
    order_submit = requests.post(configuration.URL_API_SERVICE + configuration.ORDER_SUBMIT,
                                 headers=authorization.headers_with_user_auth_token,
                                 data=json.dumps(body_for_order_submit))
    ##возвращаем номер оформленного заказа
    get_order_number = order_submit.json()['response']['id']
    print(order_submit.json())
    print(order_submit.json()['response'])
    return get_order_number
    print("Готово")
