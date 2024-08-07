import time

import pytest
import allure
from Loymax.deposit_page import DepositPage
from Loymax.login_page import LoymaxLoginPage
from Tests import steps
from Tests.steps import LoyaltyTestBase, promocode_parametrize

def test_aboba(driver):
    bb = LoymaxLoginPage(driver)
    bb.authorization()
    bb.go_to_deposit_page()
    aa = DepositPage(driver)
    aa.choose_accrual_option()
    aa.select_company()
    aa.select_currency()
    aa.fill_description_field()
    aa.fill_internal_description_field()
    aa.choose_manual_input_option()
    aa.select_id_in_list()
    aa.fill_bonus_card_field()
    aa.fill_amount_bonus_field()
    aa.fill_operation_details_field()
    aa.click_apply_button()
    aa.go_to_home_page()

@allure.issue("https://jira.pochtavip.com/secure/Tests.jspa#/testCase/LGC-T2332", "LGC-T2332")
@allure.feature("Доставлен")
@allure.story('Тест: "Доставлен" без бонусной карты, оплата наличными при получении')
@pytest.mark.no_card
@pytest.mark.delivered
@promocode_parametrize()
def test_delivered_no_bonus_pay_cash_no_bonus_card(user_no_card, driver, promocode):
    base = LoyaltyTestBase(promocode=promocode)
    base.choose_item(user_no_card)
    base.filling_out_order_data(user_no_card)
    base.order_submit(user_no_card)
    base.buyout_and_status_change(driver, "NI")


@allure.issue("https://jira.pochtavip.com/secure/Tests.jspa#/testCase/LGC-T2337", "LGC-T2337")
@allure.feature("Доставлен")
@allure.story('Тест: "Доставлен" без баллов, с картой, оплата наличными при получении')
@pytest.mark.with_card
@pytest.mark.delivered
@promocode_parametrize()
def test_delivered_no_bonus_pay_cash_have_bonus_card(user_with_card, driver, promocode):
    base = LoyaltyTestBase(promocode=promocode)
    base.choose_item(user_with_card)
    base.filling_out_order_data(user_with_card)
    base.order_submit(user_with_card)
    base.buyout_and_status_change(driver, "NI")
    history_page = base.loymax_ops(driver, user_with_card)
    base.asserts_delivered_no_bonus_have_card(history_page)


@allure.issue("https://jira.pochtavip.com/secure/Tests.jspa#/testCase/LGC-T2348", "LGC-T2348")
@allure.feature("Доставлен")
@allure.story('Тест: "Доставлен" со списанием бонусов, с картой, оплата наличными при получении')
@pytest.mark.with_card
@pytest.mark.with_bonuses
@pytest.mark.delivered
@promocode_parametrize()
def test_delivered_with_bonus_pay_cash_have_card(user_with_card, driver, promocode):
    base = LoyaltyTestBase(bonuses=True, driver=driver, promocode=promocode)
    base.choose_item(user_with_card)
    base.filling_out_order_data(user_with_card)
    base.order_submit(user_with_card)
    base.buyout_and_status_change("NI")
    history_page = base.loymax_ops(user_with_card)
    base.asserts_delivered_pay_bonus_have_card(history_page)

@allure.feature("Отказ")
@allure.story('Тест: "Отказ" без бонусной карты, оплата наличными при получении')
@pytest.mark.with_card
@pytest.mark.with_bonuses
@pytest.mark.refused
@promocode_parametrize()
def test_refused_no_bonus_pay_cash_no_card(user_no_card, driver, promocode):
    promo = steps.init_promo(promocode=promocode)
    steps.choose_item(user_no_card)
    order_number = steps.submit_and_pay(user_no_card, promocode=promo)
    steps.buyout_and_status_change(driver, order_number, "QI", promo)

@allure.issue("https://jira.pochtavip.com/secure/Tests.jspa#/testCase/LGC-T2346", "LGC-T2346")
@allure.feature("Отказ")
@allure.story('Тест: "Отказ" без баллов, с картой, оплата наличными при получении')
@pytest.mark.with_card
@pytest.mark.refused
@promocode_parametrize()
def test_refused_no_bonus_pay_cash_have_card(user_with_card, driver, promocode):
    promo = steps.init_promo(promocode=promocode)
    steps.choose_item(user_with_card)
    order_number = steps.submit_and_pay(user_with_card, promocode=promo)
    steps.buyout_and_status_change(driver, order_number, "QI", promo)
    history_page = steps.loymax_ops(driver, user_with_card)
    steps.asserts_refused_no_bonus_have_card(history_page, order_number, promo)


@allure.issue("https://jira.pochtavip.com/secure/Tests.jspa#/testCase/LGC-T2345", "LGC-T2345")
@allure.feature("Отказ")
@allure.story('Тест: "Отказ" со списанием бонусов, с картой, оплата наличными при получении')
@pytest.mark.with_card
@pytest.mark.with_bonuses
@pytest.mark.refused
@promocode_parametrize()
def test_refused_with_bonus_pay_cash_have_card(user_with_card, driver, promocode):
    promo = steps.init_promo(promocode=promocode)
    steps.choose_item(user_with_card)
    order_number = steps.submit_and_pay(user_with_card, bonuses=True, promocode=promo)
    steps.buyout_and_status_change(driver, order_number, "QI", promo)
    history_page = steps.loymax_ops(driver, user_with_card)
    steps.asserts_refused_no_bonus_have_card(history_page, order_number, promo)


@allure.issue("https://jira.pochtavip.com/secure/Tests.jspa#/testCase/LGC-T2344", "LGC-T2344")
@allure.feature("Отмена")
@allure.story('Тест: "Отмена" без баллов, с картой, оплата наличными при получении')
@pytest.mark.with_card
@pytest.mark.cancelled
@pytest.mark.no_promocode
def test_cancelled_no_bonus_pay_cash_have_card(user_with_card, driver):
    steps.choose_item(user_with_card)
    order_number = steps.submit_and_pay(user_with_card)
    steps.buyout_and_status_change(driver, order_number, "MB")
    history_page = steps.loymax_ops(driver, user_with_card)
    steps.asserts_cancelled_no_bonus_have_card(history_page, order_number)


@allure.issue("https://jira.pochtavip.com/secure/Tests.jspa#/testCase/LGC-T2335", "LGC-T2335")
@allure.feature("Отмена")
@allure.story('Тест: "Отмена" со списанием бонусов, с картой, оплата наличными при получении')
@pytest.mark.with_card
@pytest.mark.with_bonuses
@pytest.mark.cancelled
@pytest.mark.no_promocode
def test_cancelled_with_bonus_pay_cash_have_card(user_with_card, driver):
    steps.choose_item(user_with_card)
    order_number = steps.submit_and_pay(user_with_card, bonuses=True)
    steps.buyout_and_status_change(driver, order_number, "MB")
    history_page = steps.loymax_ops(driver, user_with_card)
    steps.asserts_cancelled_pay_bonus_have_card(history_page, order_number)


@allure.issue("https://jira.pochtavip.com/secure/Tests.jspa#/testCase/LGC-T2347", "LGC-T2347")
@allure.feature("Оформлен")
@allure.story('Тест: "Оформлен" без бонусной карты, оплата наличными при получении')
@pytest.mark.no_card
@pytest.mark.processed
@pytest.mark.no_promocode
def test_processed_pay_cash_no_bonus_card(user_no_card, driver):  # в черновом варианте - просто оформление заказа
    steps.choose_item(user_no_card)
    order_number = steps.submit_and_pay(user_no_card)
    steps.buyout_and_status_change(driver, order_number, "AB")


@allure.issue("https://jira.pochtavip.com/secure/Tests.jspa#/testCase/LGC-T2341", "LGC-T2341")
@allure.feature("Оформлен")
@allure.story('Тест: "Оформлен" без баллов, с картой, оплата наличными при получении')
@pytest.mark.with_card
@pytest.mark.processed
@pytest.mark.no_promocode
def test_processed_pay_cash_with_bonus_card(user_with_card, driver):  # в черновом варианте - просто оформление заказа
    steps.choose_item(user_with_card)
    order_number = steps.submit_and_pay(user_with_card)
    steps.buyout_and_status_change(driver, order_number, "AB")


@allure.issue("https://jira.pochtavip.com/secure/Tests.jspa#/testCase/LGC-T2342", "LGC-T2342")
@allure.feature("Оформлен")
@allure.story('Тест: "Оформлен" со списанием бонусов, с картой, оплата наличными при получении')
@pytest.mark.with_card
@pytest.mark.with_bonuses
@pytest.mark.processed
@pytest.mark.no_promocode
def test_processed_with_bonus_pay_cash(user_with_card, driver):
    steps.choose_item(user_with_card)
    order_number = steps.submit_and_pay(user_with_card)
    steps.buyout_and_status_change(driver, order_number, "AB")
    history_page = steps.loymax_ops(driver, user_with_card)
    steps.asserts_processed_pay_bonus_have_card(history_page, order_number)


@allure.issue("https://jira.pochtavip.com/secure/Tests.jspa#/testCase/LGC-T2334", "LGC-T2334")
@allure.feature("Частичный отказ")
@allure.story('Тест: "Частичный отказ" без бонусной карты, оплата наличными при получении')
@pytest.mark.no_card
@pytest.mark.partial_cancelled
@promocode_parametrize()
def test_partial_cancelled_pay_cash_no_bonus_card(user_no_card, driver, promocode):
    promo = steps.init_promo(promocode=promocode)
    steps.choose_two_items(user_no_card)
    order_number = steps.submit_and_pay(user_no_card, promocode=promo)
    steps.buyout_and_status_change(driver, order_number, "OI", promo)


@allure.issue("https://jira.pochtavip.com/secure/Tests.jspa#/testCase/LGC-T2339", "LGC-T2339")
@allure.feature("Частичный отказ")
@allure.story('Тест: "Частичный отказ" без баллов, с картой, оплата наличными при получении')
@pytest.mark.with_card
@pytest.mark.partial_cancelled
@promocode_parametrize()
def test_partial_cancelled_no_bonus_pay_cash_with_bonus_card(user_with_card, driver, promocode):
    promo = steps.init_promo(promocode=promocode)
    steps.choose_two_items(user_with_card)
    order_number = steps.submit_and_pay(user_with_card, promocode=promo)
    steps.buyout_and_status_change(driver, order_number, "OI", promocode=promo)
    history_page = steps.loymax_ops(driver, user_with_card)
    steps.asserts_partial_cancelled_no_bonus_have_card(history_page, order_number, promo)


@allure.issue("https://jira.pochtavip.com/secure/Tests.jspa#/testCase/LGC-T2340", "LGC-T2340")
@allure.feature("Частичный отказ")
@allure.story('Тест: "Частичный отказ" со списанием бонусов, с картой, оплата наличными при получении')
@pytest.mark.with_card
@pytest.mark.partial_cancelled
@promocode_parametrize()
def test_partial_cancelled_with_bonus_pay_cash(user_with_card, driver, promocode):
    promo = steps.init_promo(promocode=promocode)
    steps.choose_two_items(user_with_card)
    order_number = steps.submit_and_pay(user_with_card, bonuses=True, promocode=promo)
    steps.buyout_and_status_change(driver, order_number, "OI")
    history_page = steps.loymax_ops(driver, user_with_card)
    steps.asserts_partial_cancelled_pay_bonus_have_card(history_page, order_number, promo)

