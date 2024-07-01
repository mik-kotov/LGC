from API import locators_api, data
from random import randint
import json
import requests
import time


def retry(max_attempts, delay=1):
    def decorator(func):
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    print(f"Attempt {attempts} failed: {e}")
                    time.sleep(delay)
            raise RuntimeError(f"Function {func.__name__} failed after {max_attempts} attempts")
        return wrapper
    return decorator


class OrderSubmit:

    def __init__(self, api_client):
        self.order_number = None
        self.cart_data = None
        self.get_cart = None
        self.order_submit_response = None
        self.api_client = api_client
        self.bonuses = randint(1, 4)

    def open_cart(self):
        print('Открываем корзину')
        get_cart = self.api_client.get(locators_api.URL_API_SERVICE + locators_api.CART)
        self.get_cart = get_cart

    def cart_order_data(self):
        print('Просматриваем данные заказа для корзины')
        cart_data = self.api_client.get(locators_api.URL_API_SERVICE + locators_api.CART_ORDER)
        self.cart_data = cart_data

    def use_bonuses(self):
        card_number = self.api_client.user_card
        body_for_use_bonuses = {"bonus_card": f"{card_number}", "bonuses_spend_count": self.bonuses}
        post_bonuses = self.api_client.post(locators_api.URL_API_SERVICE + locators_api.POST_BONUSES,
                                       data=json.dumps(body_for_use_bonuses))
        print("Применены бонусы")
        print(f"Списано баллов: {self.bonuses}")
        return post_bonuses

    @retry(3, 20)
    def add_item_and_order_submit(self):
        body_for_order_submit = {'need_bonus_card_issue': True}
        order_submit = self.api_client.post(locators_api.URL_API_SERVICE + locators_api.ORDER_SUBMIT,
                                       data=json.dumps(body_for_order_submit))
        order_submit.raise_for_status()
        self.order_submit_response = order_submit.json()
        print("Заказ оформлен")

    def get_order_number(self):
        try:
            order_number = self.order_submit_response['response']['id']
            print(f"Номер заказа: {order_number}")
            self.order_number = order_number

        except TypeError:
            if self.order_submit_response is None:
                print("Ошибка. Тело ответа отсутствует или пусто")
            else:
                print(f"Ошибка. Тело ответа: {self.order_submit_response}")


class WriteOff:

    def __init__(self, submit, bonuses, card):
        self.write_off_response = None
        self.card = card
        self.bonuses = str(bonuses)
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
            "bonusCard": self.card,
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
        self.write_off_response = post_bonuses.json()
        return post_bonuses





