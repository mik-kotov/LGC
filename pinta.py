from API import authorization, choose_item_in_catalog, order_submit
from Bitrix import bitrix
from Loymax import login_page, user_page, call_center


api_client = authorization.api_client

def choose_item_and_submit():

    clothes_list = choose_item_in_catalog.get_products_list_sorted_by_gender()
    item_card = choose_item_in_catalog.get_item_card_from_product_list(clothes_list)
    available_item_sizes = choose_item_in_catalog.check_available_item_sizes(item_card)
    choose_item_in_catalog.add_item_in_cart(available_item_sizes)
    clothes_list = choose_item_in_catalog.get_products_list_sorted_by_gender()
    item_card = choose_item_in_catalog.get_item_card_from_product_list(clothes_list)
    available_item_sizes = choose_item_in_catalog.check_available_item_sizes(item_card)
    choose_item_in_catalog.add_item_in_cart(available_item_sizes)
    order_submit.open_cart()
    order_submit.cart_order_data()
    submit_response = order_submit.add_item_and_order_submit()
    return submit_response

def bonuses_write_off(submit_response):

    write_off = order_submit.WriteOff(submit_response)
    write_off.send_bonuses()

def status_change_and_purchase(order_id, order_status):

    order_edit_link = bitrix.order_edit_link(order_id)
    order_edit_page = bitrix.bitrix_ops(order_edit_link)
    bitrix.change_buyout_status_to_yes(order_edit_page)
    order_in_bitrix_link = bitrix.order_link(order_id)
    order_page = bitrix.bitrix_ops(order_in_bitrix_link)
    bitrix.order_status_change(order_page, order_status)

def check_loymax(order_id):

    login_Page = login_page.LoginPage()
    login_Page.authorization()
    call_center_page = call_center.CallCenterPage()
    call_center_page.go_to_search()
    call_center_page.search_user()
    user_Page = user_page.UserPage()
    user_Page.open_purchase_history()
    user_Page.order_number_is_instance(order_id)
    user_Page.confirmation_check()



order_response = choose_item_and_submit()
order_id = order_submit.get_order_number(order_response)
bonuses_write_off(order_response)
status_change_and_purchase(order_id, "NI")
check_loymax(order_id)
