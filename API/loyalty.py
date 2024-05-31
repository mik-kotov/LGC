# from API import order_submit
# from API import data
# import random
# import requests
# import pinta
# import json
#
# import locators_api
#
# class WriteOff:
#
#
#     def __init__(self, submit):
#
#         self.bonuses = str(random.randint(1, 25))
#         self.write_off_request_headers = self.write_off_headers_formation()
#         self.get_submit = submit
#         self.write_off_request_body = self.write_off_body_formation()
#
#     def write_off_body_formation(self):
#
#         write_off_request_body = {
#
#             # начало формирования тела: добавляем переменные, которые не берутся из ответа метода order/submit
#
#             "mobilePhone": data.user_phone,
#             "bonusCard": data.user_card,
#             "coupon": "",
#             "paymentAmount": self.bonuses
#         }
#         response = self.get_submit()['response']
#         product_info = response["products"][0]
#         price_info = response["price"]
#         write_off_request_body.update({
#
#             "purchaseId": response["id"],
#             "orderDatetime": response["status_date"]
#
#         })  # тут совпадают id и order_number. А если два товара? Глянуть
#
#         write_off_request_body.update({"products":
#             [{
#                 "basketId": product_info["basket_id"],
#                 "productId": product_info["product_id"],
#                 "price": price_info["total"],
#                 "count": product_info["count"],
#                 "name": product_info["name"],
#                 "amount": price_info["final"],
#                 "discount": (price_info["total"] - price_info["final"])
#             }]
#         })
#         return json.dumps(write_off_request_body)
#
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
#
#     def send_bonuses(self):
#
#         body = self.write_off_request_body
#         headers = self.write_off_request_headers
#         post_bonuses = requests.post(locators_api.URL_LOYALTY_SERVICE + locators_api.WRITE_OFF,
#                                        headers=headers,
#                                        data=body)
#         print("Применены бонусы")
#         print(f"Списано баллов: {self.bonuses}")
#         return post_bonuses
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
