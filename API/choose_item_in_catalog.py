import random
from API import locators_api


class ChooseItem:

    def __init__(self, api_client):

        self.api_client = api_client

    def get_catalog(self):

        print("Открываем каталог")
        catalog = self.api_client.get(locators_api.URL_API_SERVICE + locators_api.CATALOG)
        assert catalog.status_code == 200

    def get_category(self):

        def make_request(url):
            return self.api_client.get(locators_api.URL_API_SERVICE + locators_api.CATALOG + "/" + url).json()

        new_url = random.choice(["men", "women"])
        has_subcategories = True
        while has_subcategories:
            try:
                current_response = make_request(new_url)
                current_page = current_response['response']['categories']
                selected_category = random.choice(current_page)
                new_url = selected_category['url']
                has_subcategories = selected_category['has_subcategories']
            except (KeyError, TypeError):
                break
        self.category_url = new_url

    def get_list(self):
        def make_request(url):
            return (self.api_client.get(locators_api.URL_API_SERVICE +
                                        locators_api.CATEGORY + "/" +
                                        url +
                                        locators_api.LIST)).json()
        new_url = self.category_url
        clothes_list = []
        has_subcategories = True
        while has_subcategories:
            try:
                current_response = make_request(new_url)['response']
                current_tags = current_response['category_tags']
                if current_tags != []:
                    selected_category = random.choice(current_tags)
                    new_url = selected_category['url']
                else:
                    clothes_list = current_response['products']
                    has_subcategories = False
            except (KeyError, TypeError):
                break
        self.clothes_list = clothes_list

    def get_item_card_from_product_list(self):
        print('Открываем карточку товара')
        product_id = random.choice(
            [product['id'] for product in self.clothes_list if product['price'] > 2000]
        )

        item_card = self.api_client.get(locators_api.URL_API_SERVICE + locators_api.PRODUCT + "/" + str(product_id))
        assert item_card.status_code == 200
        self.item_card = item_card.json()

    def check_available_item_sizes(self):
        available_item_sizes = []
        while available_item_sizes == []:
            print("Проверяем доступные размеры товара")
            current_item_size_value_count = len(self.item_card['response']['sizes'])
            for i in range(current_item_size_value_count):
                if not self.item_card['response']['sizes'][i]['out_of_stock']:
                    available_item_sizes = [self.item_card['response']['sizes'][i]['id']] + available_item_sizes
                elif self.item_card['response']['sizes'][i]['out_of_stock']:
                    continue
                i += 1
        print("Товар найден")
        self.available_item_sizes = available_item_sizes

    def add_item_in_cart(self):
        print("Добавляем товар в корзину")
        count_of_items_sizes_option = len(self.available_item_sizes)
        chosen_size = self.available_item_sizes[random.randint(0, (count_of_items_sizes_option - 1))]
        add = self.api_client.post(locators_api.URL_API_SERVICE + locators_api.CART,
                                   data='{ "size_id": ' + str(chosen_size) + '}')
        assert add.status_code == 200
        print("Товар добавлен")
