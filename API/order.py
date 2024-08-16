from API import locators_api, data
from random import choice
import json
import time
from faker import Faker

fake = Faker('ru_RU')


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


class Order:

    def __init__(self, api_client):
        self.count_of_items_in_cart = None
        self.promocode_name = "июль5"
        self.price_final = None
        self.pickup_offers = None
        self.city = None
        self.use_promocode_response = None
        self.order_number = None
        self.cart_data = None
        self.get_cart = None
        self.order_submit_response = None
        self.api_client = api_client
        self.user_card = api_client.user_card
        self.bonuses = 0
        self.bonuses_balance = 0

    def reset_order(self):
        reset = self.api_client.post(locators_api.URL_API_SERVICE + locators_api.RESET_ORDER)
        assert reset.status_code == 200
        return reset

    def reset_cart(self):
        self.open_cart()
        products = self.get_cart['response']['products']
        for product in products:
            size_id = product['size']['id']
            delete_url = f"{locators_api.URL_API_SERVICE}{locators_api.CART}/{size_id}"
            response = self.api_client.delete(delete_url)
            assert response.status_code == 200

    def set_city(self):
        self.city = data.get_random_city()
        set_city = self.api_client.post(locators_api.URL_API_SERVICE + locators_api.CITY, data=json.dumps(
            {"id": self.city}))
        return set_city

    def set_pickup_point(self):
        pickup_offers = self.api_client.get(locators_api.URL_API_SERVICE + locators_api.PICKUP_OFFERS)
        point = choice(pickup_offers.json()['response'])
        point_id = point['store']['id'].split("-")
        set_request_body = {"delivery_service_id": point_id[0], "pickup_point_id": point_id[1]}
        set_pickup_point = self.api_client.post(locators_api.URL_API_SERVICE + locators_api.FIX_PICKUP_POINT,
                                                data=json.dumps(set_request_body))
        return set_pickup_point

    def set_payment_by_cash(self):
        set_payment = self.api_client.post(locators_api.URL_API_SERVICE + locators_api.PAYMENT_TYPE,
                                           data=json.dumps({"payment_type_id": "cash_upon_receipt"}))
        return set_payment

    def set_delivery_type_as_pickup(self):
        set_delivery = self.api_client.post(locators_api.URL_API_SERVICE + locators_api.DELIVERY_TYPE,
                                            data=json.dumps({"delivery_type": "pickup"}))
        return set_delivery

    def set_order_customer(self):
        name = fake.name().split(" ")
        request_body = {
            "email": fake.free_email(),
            "name": name[1],
            "patronymic": name[2],
            "phone": self.api_client.phone_number,
            "surname": name[0]
        }
        set_customer = self.api_client.post(locators_api.URL_API_SERVICE + locators_api.ORDER_CUSTOMER,
                                            data=json.dumps(request_body))
        return set_customer

    def open_cart(self):
        print('Открываем корзину')
        get_cart = self.api_client.get(locators_api.URL_API_SERVICE + locators_api.CART)
        self.get_cart = get_cart.json()
    def cart_order_data(self):
        print('Просматриваем данные заказа для корзины')
        cart_data = self.api_client.get(locators_api.URL_API_SERVICE + locators_api.CART_ORDER)
        self.cart_data = cart_data.json()

    def use_promocode(self):

        body_for_use_promo = {"promocode": self.promocode_name}
        post_promo = self.api_client.post(locators_api.URL_API_SERVICE + locators_api.POST_PROMOCODE,
                                          data=json.dumps(body_for_use_promo)).json()
        assert post_promo['response']['price']['promocode_discount'] > 0
        self.use_promocode_response = post_promo
        return post_promo

    def check_max_bonus_is_null(self):
        self.bonuses = self.get_cart['response']['price']['bonus_spend']['max_bonus_spend']
        return self.bonuses == 0

    def check_available_bonuses_is_null(self):
        available_bonuses = self.get_cart['response']['bonus_card']['available_bonuses']
        return available_bonuses < 1000

    def count_of_items_in_the_cart(self):
        self.count_of_items_in_cart = len(self.get_cart['response']['products'])
        return self.count_of_items_in_cart

    def use_bonuses(self):
        self.api_client.bonuses_balance = (self.get_cart['response']['bonus_card']['total_bonuses'] - self.bonuses)
        card_number = self.get_cart['response']['bonus_card']['number']
        body_for_use_bonuses = {"bonus_card": f"{card_number}", "bonuses_spend_count": self.bonuses}
        post_bonuses = self.api_client.post(locators_api.URL_API_SERVICE + locators_api.POST_BONUSES,
                                            data=json.dumps(body_for_use_bonuses)).json()
        print("Применены бонусыы")
        print(f"Списано баллов: {self.bonuses}")
        return post_bonuses

    def submit_an_order(self):
        body_for_order_submit = {'need_bonus_card_issue': True}
        order_submit = self.api_client.post(locators_api.URL_API_SERVICE + locators_api.ORDER_SUBMIT,
                                            data=json.dumps(body_for_order_submit))
        order_submit.raise_for_status()
        self.order_submit_response = order_submit.json()
        self.price_final = self.order_submit_response['response']['price']['final']
        print("Заказ оформлен")
        return self

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


# class WriteOff:
#
#     def __init__(self, submit, bonuses, card, promocode=None):
#         self.write_off_response = None
#         self.card = card
#         self.bonuses = str(bonuses)
#         self.write_off_request_headers = self.write_off_headers_formation()
#         self.get_submit = submit
#         if promocode:
#             self.write_off_request_body = self.write_off_body_formation(promocode.name)
#         else:
#             self.write_off_request_body = self.write_off_body_formation("")
#
#     def write_off_body_formation(self, promocode):
#         print(promocode)
#         print(int(self.bonuses))
#         write_off_request_body = {
#             "coupon": promocode,
#             "paymentAmount": int(self.bonuses)
#         }
#
#         response_core = self.get_submit['response']
#         products_info = response_core["products"]
#         price_info = response_core["price"]
#
#         write_off_request_body.update({
#             "mobilePhone": response_core["customer"]["phone"][1:],
#             "bonusCard": self.card,
#             "purchaseId": response_core["id"],
#             "orderDatetime": response_core["creation_date"]
#         })
#
#         def extract_goods(inp):
#             parts = inp.split('-')
#             if len(parts) > 1:
#                 return int(parts[0])
#             else:
#                 return int(inp)
#
#         products = []
#         for product_info in products_info:
#             goods_id = extract_goods(product_info["product_code"])
#             products.append({
#                 "basketId": product_info["basket_id"],
#                 "productId": goods_id,
#                 "price": product_info["price"],
#                 "count": product_info["count"],
#                 "name": product_info["name"],
#                 "amount": product_info["price"] * product_info["count"],
#                 "discount": product_info["old_price"] - product_info["price"]
#             })
#
#         write_off_request_body["products"] = products
#         print('write off request body:')
#         print(write_off_request_body)
#         return json.dumps(write_off_request_body)
#
#     def write_off_headers_formation(self):
#
#         get_ip = requests.get('http://jsonip.com')
#         ip = get_ip.json()['ip']
#         write_off_request_headers = {
#             **data.headers,
#             "X-Forwarded-For": ip,
#             "X-Auth-Token": "7c9d8f00ea0ddd9e02cab3eb2b3bd0d1"
#
#             }
#         return write_off_request_headers
#
#     def send_bonuses(self):
#
#         body = self.write_off_request_body
#         print(self.write_off_request_body)
#         headers = self.write_off_request_headers
#         post_bonuses = requests.post(locators_api.URL_LOYALTY_SERVICE + locators_api.WRITE_OFF,
#                                        headers=headers,
#                                        data=body)
#         print("Применены бонусы")
#         print(f"Списано баллов: {self.bonuses}")
#         self.write_off_response = post_bonuses.json()
#         print(post_bonuses.json())
#         return post_bonuses


class PromoCode:
    def __init__(self):
        self.name = "июль5"
        self.order_sum = None
