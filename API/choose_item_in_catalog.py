import random
from API import locators_api
from API import authorization



api_client = authorization.api_client
def get_products_list_sorted_by_gender():
    catalog_gender = random.choice(["/men", "/women"])
    current_gender = catalog_gender
    print(f"Открываем каталог с сортировкой по полу: {current_gender}")
    clothes_list = api_client.get(locators_api.URL_API_SERVICE + locators_api.CATEGORY + current_gender + locators_api.LIST)
    return clothes_list.json()


def get_item_card_from_product_list(clothes_list):

    print('Открываем карточку товара')
    product_id = clothes_list['response']['products'][random.randint(1,5)]['id']
    item_card = api_client.get(locators_api.URL_API_SERVICE + locators_api.PRODUCT +"/" + str(product_id))
    return item_card.json()


def check_available_item_sizes(item_card):
    available_item_sizes = []
    while available_item_sizes == []:
        print("Проверяем доступные размеры товара")
        # считаем количество предлагаемых цветоразмеров
        current_item_size_value_count = len(item_card['response']['sizes'])
        #Проверяем доступность каждого цветоразмера
        for i in range(current_item_size_value_count):
            if item_card['response']['sizes'][i]['out_of_stock'] == False:
                available_item_sizes = [item_card['response']['sizes'][i]['id']] + available_item_sizes
            elif item_card['response']['sizes'][i]['out_of_stock'] == True:
                continue
            i +=1
    #если нет ни одного доступного цветоразмера, всё ломается. Пофиксить
    print("Товар найден")
    #возвращаем список доступных цветоразмеров
    return available_item_sizes

def add_item_in_cart(item_sizes_options):
    #смотрим размеры выбранного товара
    print("Добавляем товар в корзину")
    count_of_items_sizes_option = len(item_sizes_options)
    #случайным образом выбираем один из них
    chosen_size = item_sizes_options[random.randint(0,  (count_of_items_sizes_option -1))]
    #добавляем его в корзину
    api_client.post(locators_api.URL_API_SERVICE + locators_api.CART, data='{ "size_id": ' + str(chosen_size) + '}')
    print("Товар добавлен")

 return post_bonuses