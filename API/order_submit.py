from API import locators_api, data
from random import randint
import json
import requests

class OrderSubmit:

    def __init__(self, api_client):
        self.api_client = api_client


    def open_cart(self):
        print('Открываем корзину')
        get_cart = self.api_client.get(locators_api.URL_API_SERVICE + locators_api.CART)
        self.get_cart = get_cart

    def cart_order_data(self):
        print('Просматриваем данные заказа для корзины')
        cart_data = self.api_client.get(locators_api.URL_API_SERVICE + locators_api.CART_ORDER)
        self.cart_data = cart_data

    # def use_bonuses():
    #     card_number = data.user_card # cделать умнее
    #     bonuses_to_spend = randint(1,20)
    #     body_for_use_bonuses = {"bonus_card": f"{card_number}", "bonuses_spend_count": bonuses_to_spend}
    #     post_bonuses = api_client.post(locators_api.URL_API_SERVICE + locators_api.ORDER_SUBMIT,
    #                                    data=json.dumps(body_for_use_bonuses))
    #     print("Применены бонусы")
    #     print(f"Списано баллов: {bonuses_to_spend}")
    #     return post_bonuses

    def add_item_and_order_submit(self):

        body_for_order_submit = {'need_bonus_card_issue': True}
        order_submit = self.api_client.post(locators_api.URL_API_SERVICE + locators_api.ORDER_SUBMIT,
                                       data=json.dumps(body_for_order_submit))
        order_submit_response = order_submit.json()
        print("Заказ оформлен")
        self.order_submit_response = order_submit_response

    def get_order_number(self):

        order_number = self.order_submit_response['response']['id']
        print(f"Номер заказа: {order_number}")
        self.order_number = order_number


class WriteOff:

    def __init__(self, submit, card):

        self.bonuses = str(randint(1, 3))
        self.write_off_request_headers = self.write_off_headers_formation()
        self.get_submit = submit
        self.write_off_request_body = self.write_off_body_formation()

    def write_off_body_formation(self):
        write_off_request_body = {
            "coupon": "",
            "paymentAmount": self.bonuses
        }

        response_core = self.get_submit['response']
        products_info = response_core["products"]
        price_info = response_core["price"]

        write_off_request_body.update({
            "mobilePhone": response_core["customer"]["phone"][1:],
            "bonusCard": data.user_card,
            "purchaseId": response_core["id"],
            "orderDatetime": response_core["creation_date"]
        })

        def extract_goods(inp):
            parts = inp.split('-')
            if len(parts) > 1:
                return int(parts[0])
            else:
                return int(inp)

        products = []
        for product_info in products_info:
            goods_id = extract_goods(product_info["product_code"])
            products.append({
                "basketId": product_info["basket_id"],
                "productId": goods_id,
                "price": product_info["price"],
                "count": product_info["count"],
                "name": product_info["name"],
                "amount": product_info["price"] * product_info["count"],
                "discount": product_info["old_price"] - product_info["price"]
            })

        write_off_request_body["products"] = products

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


def extract_number(input_str):
    parts = input_str.split('-')
    if len(parts) > 1:
        return int(parts[0])
    else:
        return int(input_str)


# Пример использования


