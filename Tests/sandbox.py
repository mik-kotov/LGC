# from selenium.webdriver.chrome.service import Service
# from selenium import webdriver
# import pytest
# from API.authorization import APIClient
# from API import catalog, order, data
# from Bitrix.bitrix import Bitrix
# from Loymax import login_page, user_page, call_center
# import time
#
# @pytest.yield_fixture(scope='session')
# def browser():
#     print("")
#     chrome_driver_path = r'C:\chromedriver\chromedriver.exe'
#     options = webdriver.ChromeOptions()
#     options.add_argument("--start-maximized")
#     #options.add_argument("--headless")
#     service = Service(chrome_driver_path)
#     driver = webdriver.Chrome(service=service, options=options)
#     yield driver
#     driver.quit()
#
#
# def delivered_with_bonus_pay_cash():
#     user = data.user_with_card_phone
#     card = data.user_card
#     user_with_card = APIClient(user, card)
#     search_item = choose_item_in_catalog.ChooseItem(user_with_card)
#     search_item.get_catalog()
#     search_item.get_category()
#     search_item.get_list()
#     search_item.get_item_card_from_product_list()
#     search_item.check_available_item_sizes()
#     search_item.add_item_in_cart()
#     submit = order_submit.Order(user_with_card)
#     submit.open_cart()
#     submit.cart_order_data()
#     submit.use_bonuses()
#     submit.add_item_and_order_submit()
#     submit.get_order_number()
#     pay_bonuses = order_submit.WriteOff(submit.order_submit_response, submit.bonuses)
#     pay_bonuses.send_bonuses()
#     order_number = submit.order_number
#     print(order_number)
#
#
#
# # def pay_cash():
# #     user = data.user_no_card_phone
# #     user_with_card = APIClient(user)
# #     search_item = choose_item_in_catalog.ChooseItem(user_with_card)
# #     search_item.get_catalog()
# #     search_item.get_category()
# #     search_item.get_list()
# #     search_item.get_item_card_from_product_list()
# #     search_item.check_available_item_sizes()
# #     search_item.add_item_in_cart()
# #     print(search_item.available_item_sizes)
# #
# #
# # def test_change_to_yes(driver):
# #     user = data.user_with_card_phone
# #     card = data.user_card
# #     user_with_card = APIClient(user, card)
# #     search_item = choose_item_in_catalog.ChooseItem(user_with_card)
# #     search_item.get_catalog()
# #     search_item.get_category()
# #     search_item.get_list()
# #     search_item.get_item_card_from_product_list()
# #     search_item.check_available_item_sizes()
# #     search_item.add_item_in_cart()
# #     submit = order_submit.OrderSubmit(user_with_card)
# #     submit.open_cart()
# #     submit.cart_order_data()
# #     submit.use_bonuses()
# #     submit.add_item_and_order_submit()
# #     submit.get_order_number()
# #     pay_bonuses = order_submit.WriteOff(submit.order_submit_response, submit.bonuses)
# #     pay_bonuses.send_bonuses()
# #     order_number = submit.order_number
# #     bitrix_ops = Bitrix(driver)
# #     bitrix_ops.authorization()
# #     bitrix_ops.open(Bitrix.order_edit_link(order_number))
# #     bitrix_ops.change_buyout_status_to_yes()
# #     time.sleep(10)
#
# def adelivered_with_bonus_pay_cash():
#     user_n_card = data.get_random_user_with_card()
#     card = user_n_card[1]
#     user = user_n_card[0]
#     user_with_card = APIClient(user, card)
#     search_item = choose_item_in_catalog.ChooseItem(user_with_card)
#     search_item.get_catalog()
#     search_item.get_category()
#     search_item.get_list()
#     search_item.get_item_card_from_product_list()
#     search_item.check_available_item_sizes()
#     search_item.add_item_in_cart()
#
# for a in range(50):
#     adelivered_with_bonus_pay_cash()
#
#     # login_Page = login_page.LoymaxLoginPage(driver)
#     # login_Page.authorization()
#     # call_center_page = call_center.CallCenterPage(driver)
#     #
#     # call_center_page.go_to_search()
#     # call_center_page.search_user()
#     # user_Page = user_page.UserPage(driver)
#     # user_Page.open_purchase_history()
#     # user_Page.order_number_is_instance(order_number)
#     # user_Page.cancellation_check()

# oo = "boxberry-03116"
# print(oo[:-])