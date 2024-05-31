from API import locators_api, data, authorization
from random import randint
import json
import requests


api_client = authorization.api_client
def open_cart():
    print('Открываем корзину')
    get_cart = api_client.get(locators_api.URL_API_SERVICE + locators_api.CART)
    return get_cart
def cart_order_data():
    print('Просматриваем данные заказа для корзины')
    cart_data = api_client.get(locators_api.URL_API_SERVICE + locators_api.CART_ORDER)
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
    order_submit_response = order_submit.json()
    print("Заказ оформлен")

    return order_submit_response

def get_order_number(order_submit_response):

    order_number = order_submit_response['response']['id']
    print(f"Номер заказа: {order_number}")
    return order_number

class WriteOff:


    def __init__(self, submit):

        self.bonuses = str(randint(1, 25))
        self.write_off_request_headers = self.write_off_headers_formation()
        self.get_submit = submit
        self.write_off_request_body = self.write_off_body_formation()

    def write_off_body_formation(self):

        write_off_request_body = {

            # начало формирования тела: добавляем переменные, которые не берутся из ответа метода order/submit

            "mobilePhone": data.user_phone,
            "bonusCard": data.user_card,
            "coupon": "",
            "paymentAmount": self.bonuses
        }

        response_core = self.get_submit['response']
        product_info = response_core["products"][0]
        price_info = response_core["price"]
        write_off_request_body.update({

            "purchaseId": response_core["id"],
            "orderDatetime": response_core["status_date"]

        })  # тут совпадают id и order_number. А если два товара? Глянуть

        write_off_request_body.update({"products":
            [{
                "basketId": product_info["basket_id"],
                "productId": product_info["product_id"],
                "price": price_info["total"],
                "count": product_info["count"],
                "name": product_info["name"],
                "amount": price_info["final"],
                "discount": (price_info["total"] - price_info["final"])
            }]
        })
        return json.dumps(write_off_request_body)


    def write_off_headers_formation(self):

        get_ip = requests.get('http://jsonip.com')
        ip = get_ip.json()['ip']
        write_off_request_headers = {
            **data.headers,
            "X-Forwarded-For": ip,
            "X-Auth-Token": "7c9d8f00ea0ddd9e02cab3eb2b3bd0d1"

            }
        return write_off_request_headers


    def send_bonuses(self):

        body = self.write_off_request_body
        headers = self.write_off_request_headers
        post_bonuses = requests.post(locators_api.URL_LOYALTY_SERVICE + locators_api.WRITE_OFF,
                                       headers=headers,
                                       data=body)
        print("Применены бонусы")
        print(f"Списано баллов: {self.bonuses}")
        return post_bonuses





