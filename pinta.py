from API import authorization, choose_item_in_catalog, order_submit
from Bitrix import bitrix
import Loymax

api_client = authorization.api_client

clothes_list = choose_item_in_catalog.get_products_list_sorted_by_gender()
item_card = choose_item_in_catalog.get_item_card_from_product_list(clothes_list)
available_item_sizes = choose_item_in_catalog.check_available_item_sizes(item_card)
choose_item_in_catalog.add_item_in_cart(available_item_sizes)
order_submit.open_cart()
order_submit.cart_order_data()
order_submit.use_bonuses()
order_id = order_submit.add_item_and_order_submit()
order_edit_link = bitrix.order_edit_link(order_id)
order_edit_page = bitrix.bitrix_ops(order_edit_link)
bitrix.change_buyout_status_to_yes(order_edit_page)
order_in_bitrix_link = bitrix.order_link(order_id)
order_page = bitrix.bitrix_ops(order_in_bitrix_link)
bitrix.order_status_change(order_page, "NI")