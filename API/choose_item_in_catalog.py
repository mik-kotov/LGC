import random
from API import configuration
import requests
from API import data
import json
from API import authorization


catalog_gender = random.choice(["/men", "/women"])

def get_products_list_sorted_by_gender():
    current_gender = catalog_gender
    print(f"Открываем каталог с сортировкой по полу: {current_gender}")
    clothes_list = requests.get(configuration.URL_API_SERVICE + configuration.CATEGORY + current_gender + configuration.LIST,
              headers=authorization.headers_with_user_auth_token)
    return  clothes_list.json()


def get_item_card_from_product_list():
    list = get_products_list_sorted_by_gender()
    print('Открываем карточку товара')
    product_id = list['response']['products'][random.randint(1,10)]['id']
    item_card = requests.get(configuration.URL_API_SERVICE + configuration.PRODUCT +"/" + str(product_id),
                 headers=authorization.headers_with_user_auth_token)
    return item_card.json()

def check_available_item_sizes():
    available_item_sizes = []
    while available_item_sizes == []:
        item_card = get_item_card_from_product_list()
        print("Проверяем доступные размеры товара")
        # считаем количество предлагаемых цветоразмеров
        current_item_size_value_count = len(item_card['response']['sizes'])
        #Проверяем доступность каждого цветоразмера
        for i in range(current_item_size_value_count):
            if item_card['response']['sizes'][i]['out_of_stock'] == False:
                available_item_sizes = [ item_card['response']['sizes'][i]['id'] ] + available_item_sizes
            elif item_card['response']['sizes'][i]['out_of_stock'] == True:
                continue
            i +=1
    #если нет ни одного доступного цветоразмера, всё жестко взрывается и мир захватывают роботы. Пофиксить
    print("Товар найден")
    #возвращаем список доступных цветоразмеров
    return available_item_sizes

def add_item_in_cart():
    #смотрим размеры выбранного товара
    item_sizes_options = check_available_item_sizes()
    print("Добавляем товар в корзину")
    count_of_items_sizes_option = len(item_sizes_options)
    #случайным образом выбираем один из них
    choosen_size = item_sizes_options[random.randint(0,  (count_of_items_sizes_option -1))]
    #добавляем его в корзину
    add_item_in_cart_response = requests.post(configuration.URL_API_SERVICE + configuration.CART,
                 headers=authorization.headers_with_user_auth_token,
                                              data='{ "size_id": ' + str(choosen_size) + '}')
    print("Товар добавлен")

