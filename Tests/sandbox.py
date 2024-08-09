import json

get_cart = {"response": {
    "id": 1235270,
    "bonus_card": {
        "number": "7780004788012477895",
        "total_bonuses": 5102,
        "available_bonuses": 4859,
        "can_spend_bonuses": true,
        "percent_from_new_collection": 10,
        "percent_from_sale": 3,
        "purchases_amou
            nt":12751,
              "min_amount_for_card": 0,
        "max_amount_for_card": 99999,
        "card_update_date": "2025-02-08T00:00:00",
        "hex": "#cfcfcf",
        "type_description": "Серебряный",
        "next_level_type_description": "золотого",
        "state": "active",
        "te
            xt_for_status":"Для перехода на следующий уровень карты не хватает 87249 ₽ до
08.02
.2025
"
},
"products": [
    {
        "id": 1152986,
        "basket_id": 1152986,
        "product_id": 1151918,
        "name": "Джинсовая куртка",
        "brand": {
            "id": "levis",
            "name": "LEVI'S"
        },
        "sku": "72334-0573",
        "size": {
            "id": 1152986,
            "size_value": [
                {
                    "type": "default",
                    "value": "54",
                    "label": "RU"
                }
            ],
            "out_of_stock": false,
            "product_code": "481035-046",
            "height_values": [

            ],
            "insole": "None",
            "offline": "Fals
            e",
             "online":false
},
"color": {"hex": "0000FF","image": "","title": "Синий","draw_border": false},"count": 1,"price": 13475,"old_price": 19250,"image": "https://lgcity.ru/upload/WEB/48/10/35/481035_1.jpg","state_message": "None","tax_price": 0,"tax": 0,"in_favorites": false,"product_code": "481035"}]}


print(type(get_cart))

print(len(get_cart['response']['products']))
