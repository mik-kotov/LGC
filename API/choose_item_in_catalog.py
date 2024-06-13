import random
from API import locators_api


class ChooseItem:

    def __init__(self, api_client):

        self.api_client = api_client

    def get_catalog(self):
        print("Открываем каталог")
        catalog = self.api_client.get(locators_api.URL_API_SERVICE + "/catalog")
        assert catalog.status_code == 200


    def get_products_list_sorted_by_gender(self):
        catalog_gender = random.choice(["/men", "/women"])
        current_gender = catalog_gender
        print(f"Открываем каталог с сортировкой по полу: {current_gender}")
        clothes_list = self.api_client.get(locators_api.URL_API_SERVICE + locators_api.CATEGORY + current_gender + locators_api.LIST)
        assert clothes_list.status_code == 200
        self.clothes_list = clothes_list.json()


    def get_item_card_from_product_list(self):
        print('Открываем карточку товара')
        product_id = self.clothes_list['response']['products'][random.randint(1,5)]['id']
        item_card = self.api_client.get(locators_api.URL_API_SERVICE + locators_api.PRODUCT +"/" + str(product_id))
        assert item_card.status_code == 200
        self.item_card = item_card.json()

    def check_available_item_sizes(self):
        available_item_sizes = []
        while available_item_sizes == []:
            print("Проверяем доступные размеры товара")
            # считаем количество предлагаемых цветоразмеров
            current_item_size_value_count = len(self.item_card['response']['sizes'])
            #Проверяем доступность каждого цветоразмера
            for i in range(current_item_size_value_count):
                if self.item_card['response']['sizes'][i]['out_of_stock'] == False:
                    available_item_sizes = [self.item_card['response']['sizes'][i]['id']] + available_item_sizes
                elif self.item_card['response']['sizes'][i]['out_of_stock'] == True:
                    continue
                i +=1
        #если нет ни одного доступного цветоразмера, всё ломается. Пофиксить
        print("Товар найден")
        #возвращаем список доступных цветоразмеров
        self.available_item_sizes = available_item_sizes

    def add_item_in_cart(self):
        #смотрим размеры выбранного товара
        print("Добавляем товар в корзину")
        count_of_items_sizes_option = len(self.available_item_sizes)
        #случайным образом выбираем один из них
        chosen_size = self.available_item_sizes[random.randint(0,  (count_of_items_sizes_option -1))]
        #добавляем его в корзину
        add = self.api_client.post(locators_api.URL_API_SERVICE + locators_api.CART, data='{ "size_id": ' + str(chosen_size) + '}')
        assert add.status_code == 200
        print("Товар добавлен")

