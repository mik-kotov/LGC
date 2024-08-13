import time
import pytest
import allure
from Loymax.deposit_page import DepositPage
from Loymax.login_page import LoymaxLoginPage
from Tests import steps
from Tests.steps import LoyaltyTestBase, promocode_parametrize

@allure.issue("https://jira.pochtavip.com/secure/Tests.jspa#/testCase/LGC-T2332", "LGC-T2332")
@allure.feature("Доставлен")
@allure.story('Тест: "Доставлен" без бонусной карты, оплата наличными при получении')
@pytest.mark.no_card
@pytest.mark.delivered
@promocode_parametrize()
def test_delivered_no_bonus_pay_cash_no_bonus_card(user_no_card, driver, promocode):
    base = LoyaltyTestBase(driver, promocode)
    base.choose_item(user_no_card)
    base.order_submit(user_no_card)
    base.buyout_and_status_change("NI")


@allure.issue("https://jira.pochtavip.com/secure/Tests.jspa#/testCase/LGC-T2337", "LGC-T2337")
@allure.feature("Доставлен")
@allure.story('Тест: "Доставлен" без баллов, с картой, оплата наличными при получении')
@pytest.mark.with_card
@pytest.mark.no_bonuses
@pytest.mark.delivered
@promocode_parametrize()
def test_delivered_no_bonus_pay_cash_have_bonus_card(user_with_card, driver, promocode):
    base = LoyaltyTestBase(driver, promocode)
    base.choose_item(user_with_card)
    base.order_submit(user_with_card)
    base.buyout_and_status_change("NI")
    history_page = base.loymax_ops(user_with_card)
    base.asserts_delivered_no_bonus_have_card(history_page)


@allure.issue("https://jira.pochtavip.com/secure/Tests.jspa#/testCase/LGC-T2348", "LGC-T2348")
@allure.feature("Доставлен")
@allure.story('Тест: "Доставлен" со списанием бонусов, с картой, оплата наличными при получении')
@pytest.mark.with_card
@pytest.mark.with_bonuses
@pytest.mark.delivered
@promocode_parametrize()
def test_delivered_with_bonus_pay_cash_have_card(user_with_card, driver, promocode):
    base = LoyaltyTestBase(driver, promocode, bonuses=True)
    base.choose_item(user_with_card)
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
    base = LoyaltyTestBase(driver, promocode)
    base.choose_item(user_no_card)
    base.order_submit(user_no_card)
    base.buyout_and_status_change("QI")

@allure.issue("https://jira.pochtavip.com/secure/Tests.jspa#/testCase/LGC-T2346", "LGC-T2346")
@allure.feature("Отказ")
@allure.story('Тест: "Отказ" без баллов, с картой, оплата наличными при получении')
@pytest.mark.with_card
@pytest.mark.refused
@promocode_parametrize()
def test_refused_no_bonus_pay_cash_have_card(user_with_card, driver, promocode):
    base = LoyaltyTestBase(driver, promocode)
    base.choose_item(user_with_card)
    base.order_submit(user_with_card)
    base.buyout_and_status_change("QI")
    history_page = base.loymax_ops(user_with_card)
    base.asserts_refused_no_bonus_have_card(history_page)



@allure.issue("https://jira.pochtavip.com/secure/Tests.jspa#/testCase/LGC-T2345", "LGC-T2345")
@allure.feature("Отказ")
@allure.story('Тест: "Отказ" со списанием бонусов, с картой, оплата наличными при получении')
@pytest.mark.with_card
@pytest.mark.with_bonuses
@pytest.mark.refused
@promocode_parametrize()
def test_refused_with_bonus_pay_cash_have_card(user_with_card, driver, promocode):
    base = LoyaltyTestBase(driver, promocode, bonuses=True)
    base.choose_item(user_with_card)
    base.order_submit(user_with_card)
    base.buyout_and_status_change("QI")
    history_page = base.loymax_ops(user_with_card)
    base.asserts_refused_no_bonus_have_card(history_page)


@allure.issue("https://jira.pochtavip.com/secure/Tests.jspa#/testCase/LGC-T2344", "LGC-T2344")
@allure.feature("Отмена")
@allure.story('Тест: "Отмена" без баллов, с картой, оплата наличными при получении')
@pytest.mark.with_card
@pytest.mark.cancelled
@pytest.mark.no_promocode
def test_cancelled_no_bonus_pay_cash_have_card(user_with_card, driver):
    base = LoyaltyTestBase(driver)
    base.choose_item(user_with_card)
    base.order_submit(user_with_card)
    base.buyout_and_status_change("MB")
    history_page = base.loymax_ops(user_with_card)
    base.asserts_cancelled_no_bonus_have_card(history_page)


@allure.issue("https://jira.pochtavip.com/secure/Tests.jspa#/testCase/LGC-T2335", "LGC-T2335")
@allure.feature("Отмена")
@allure.story('Тест: "Отмена" со списанием бонусов, с картой, оплата наличными при получении')
@pytest.mark.with_card
@pytest.mark.with_bonuses
@pytest.mark.cancelled
@pytest.mark.no_promocode
def test_cancelled_with_bonus_pay_cash_have_card(user_with_card, driver):
    base = LoyaltyTestBase(driver, bonuses=True)
    base.choose_item(user_with_card)
    base.order_submit(user_with_card)
    base.buyout_and_status_change("MB")
    history_page = base.loymax_ops(user_with_card)
    base.asserts_cancelled_pay_bonus_have_card(history_page)


@allure.issue("https://jira.pochtavip.com/secure/Tests.jspa#/testCase/LGC-T2347", "LGC-T2347")
@allure.feature("Оформлен")
@allure.story('Тест: "Оформлен" без бонусной карты, оплата наличными при получении')
@pytest.mark.no_card
@pytest.mark.processed
@pytest.mark.no_promocode
def test_processed_pay_cash_no_bonus_card(user_no_card, driver):  # в черновом варианте - просто оформление заказа
    base = LoyaltyTestBase(driver)
    base.choose_item(user_no_card)
    base.order_submit(user_no_card)
    base.buyout_and_status_change("AB")


@allure.issue("https://jira.pochtavip.com/secure/Tests.jspa#/testCase/LGC-T2341", "LGC-T2341")
@allure.feature("Оформлен")
@allure.story('Тест: "Оформлен" без баллов, с картой, оплата наличными при получении')
@pytest.mark.with_card
@pytest.mark.processed
@pytest.mark.no_promocode
def test_processed_pay_cash_with_bonus_card(user_with_card, driver):  # в черновом варианте - просто оформление заказа
    base = LoyaltyTestBase(driver)
    base.choose_item(user_with_card)
    base.order_submit(user_with_card)
    base.buyout_and_status_change("AB")


@allure.issue("https://jira.pochtavip.com/secure/Tests.jspa#/testCase/LGC-T2342", "LGC-T2342")
@allure.feature("Оформлен")
@allure.story('Тест: "Оформлен" со списанием бонусов, с картой, оплата наличными при получении')
@pytest.mark.with_card
@pytest.mark.with_bonuses
@pytest.mark.processed
@pytest.mark.no_promocode
def test_processed_with_bonus_pay_cash(user_with_card, driver):
    base = LoyaltyTestBase(driver, bonuses=True)
    base.choose_item(user_with_card)
    base.order_submit(user_with_card)
    base.buyout_and_status_change("AB")
    history_page = base.loymax_ops(user_with_card)
    base.asserts_processed_pay_bonus_have_card(history_page)


@allure.issue("https://jira.pochtavip.com/secure/Tests.jspa#/testCase/LGC-T2334", "LGC-T2334")
@allure.feature("Частичный отказ")
@allure.story('Тест: "Частичный отказ" без бонусной карты, оплата наличными при получении')
@pytest.mark.no_card
@pytest.mark.partial_cancelled
@promocode_parametrize()
def test_partial_cancelled_pay_cash_no_bonus_card(user_no_card, driver, promocode):
    base = LoyaltyTestBase(driver, promocode)
    base.choose_two_items(user_no_card)
    base.order_submit(user_no_card)
    base.buyout_and_status_change("OI")


@allure.issue("https://jira.pochtavip.com/secure/Tests.jspa#/testCase/LGC-T2339", "LGC-T2339")
@allure.feature("Частичный отказ")
@allure.story('Тест: "Частичный отказ" без баллов, с картой, оплата наличными при получении')
@pytest.mark.with_card
@pytest.mark.partial_cancelled
@promocode_parametrize()
def test_partial_cancelled_no_bonus_pay_cash_with_bonus_card(user_with_card, driver, promocode):
    base = LoyaltyTestBase(driver, promocode)
    base.choose_two_items(user_with_card)
    base.order_submit(user_with_card)
    base.buyout_and_status_change("OI")
    history_page = base.loymax_ops(user_with_card)
    base.asserts_partial_cancelled_no_bonus_have_card(history_page)


@allure.issue("https://jira.pochtavip.com/secure/Tests.jspa#/testCase/LGC-T2340", "LGC-T2340")
@allure.feature("Частичный отказ")
@allure.story('Тест: "Частичный отказ" со списанием бонусов, с картой, оплата наличными при получении')
@pytest.mark.with_card
@pytest.mark.partial_cancelled
@promocode_parametrize()
def test_partial_cancelled_with_bonus_pay_cash(user_with_card, driver, promocode):
    base = LoyaltyTestBase(driver, promocode, bonuses=True)
    base.choose_two_items(user_with_card)
    base.order_submit(user_with_card)
    base.buyout_and_status_change("OI")
    history_page = base.loymax_ops(user_with_card)
    base.asserts_partial_cancelled_pay_bonus_have_card(history_page)

