from API import order_submit
from API import data
import random
import pinta
import json


class BonusesOps:

    @staticmethod
    def write_off_body_formation(order_submit_response):
        write_off_request_body = {"mobilePhone": data.user_phone, "bonusCard": data.user_card, "coupon": "",
                "paymentAmount": str(random.randint(1, 25))}
        response = order_submit_response['response']
        product_info = response["products"][0]
        price_info = response["price"]
        write_off_request_body.update({"purchaseId": response["id"], "orderDatetime": response[
            "status_date"]})  # тут совпадают id и order_number. А если два товара? Глянуть
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
        return write_off_request_body


resp = pinta.choose_item_and_submit_no_bonuses()
current_body = json.dumps(BonusesOps.write_off_body_formation(resp))
print(current_body)

