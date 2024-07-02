import pytest
import allure
import steps


@allure.issue("https://jira.pochtavip.com/secure/Tests.jspa#/testCase/LGC-T2332", "LGC-T2332")
@allure.feature("Доставлен")
@allure.story('Тест: "Доставлен" без бонусной карты, оплата наличными при получении')
@pytest.mark.no_card
@pytest.mark.delivered
#@pytest.mark.parametrize("promocode", [True, False])
def test_delivered_no_bonus_pay_cash_no_bonus_card(user_no_card, driver):#, promocode):
    steps.choose_item(user_no_card)
    order_number = steps.submit_and_pay(user_no_card)#, promocode=promocode)
    steps.buyout_and_status_change(driver, order_number, "NI")


@allure.issue("https://jira.pochtavip.com/secure/Tests.jspa#/testCase/LGC-T2337", "LGC-T2337")
@allure.feature("Доставлен")
@allure.story('Тест: "Доставлен" без баллов, с картой, оплата наличными при получении')
@pytest.mark.with_card
@pytest.mark.delivered
@pytest.mark.parametrize("promocode", [True, False])
def test_delivered_no_bonus_pay_cash_have_bonus_card(user_with_card, driver, promocode):

    steps.choose_item(user_with_card)
    order_number = steps.submit_and_pay(user_with_card, bonuses=False, promocode=promocode)
    steps.buyout_and_status_change(driver, order_number, "NI")
    history_page = steps.loymax_ops(driver, user_with_card)
    steps.asserts_delivered_no_bonus_have_card(history_page, order_number)


@allure.issue("https://jira.pochtavip.com/secure/Tests.jspa#/testCase/LGC-T2348", "LGC-T2348")
@allure.feature("Доставлен")
@allure.story('Тест: "Доставлен" со списанием бонусов, с картой, оплата наличными при получении')
@pytest.mark.with_card
@pytest.mark.with_bonuses
@pytest.mark.delivered
@pytest.mark.parametrize("promocode", [True, False])
def test_delivered_with_bonus_pay_cash_have_card(user_with_card, driver, promocode):

    steps.choose_item(user_with_card)
    order_number = steps.submit_and_pay(user_with_card, bonuses=True, promocode=promocode)
    steps.buyout_and_status_change(driver, order_number, "NI")
    history_page = steps.loymax_ops(driver, user_with_card)
    steps.asserts_delivered_pay_bonus_have_card(history_page, order_number)


@allure.issue("https://jira.pochtavip.com/secure/Tests.jspa#/testCase/LGC-T2346", "LGC-T2346")
@allure.feature("Отказ")
@allure.story('Тест: "Отказ" без баллов, с картой, оплата наличными при получении')
@pytest.mark.with_card
@pytest.mark.refused
def test_refused_no_bonus_pay_cash_have_card(user_with_card, driver):
    steps.choose_item(user_with_card)
    order_number = steps.submit_and_pay(user_with_card, bonuses=False)
    steps.buyout_and_status_change(driver, order_number, "QI")
    history_page = steps.loymax_ops(driver, user_with_card)
    steps.asserts_refused_no_bonus_have_card(history_page, order_number)


@allure.issue("https://jira.pochtavip.com/secure/Tests.jspa#/testCase/LGC-T2345", "LGC-T2345")
@allure.feature("Отказ")
@allure.story('Тест: "Отказ" со списанием бонусов, с картой, оплата наличными при получении')
@pytest.mark.with_card
@pytest.mark.with_bonuses
@pytest.mark.refused
def test_refused_with_bonus_pay_cash_have_card(user_with_card, driver):
    steps.choose_item(user_with_card)
    order_number = steps.submit_and_pay(user_with_card, bonuses=True)
    steps.buyout_and_status_change(driver, order_number, "QI")
    history_page = steps.loymax_ops(driver, user_with_card)
    steps.asserts_refused_no_bonus_have_card(history_page, order_number)


@allure.issue("https://jira.pochtavip.com/secure/Tests.jspa#/testCase/LGC-T2344", "LGC-T2344")
@allure.feature("Отмена")
@allure.story('Тест: "Отмена" без баллов, с картой, оплата наличными при получении')
@pytest.mark.with_card
@pytest.mark.cancelled
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
def test_processed_pay_cash_no_bonus_card(user_no_card, driver):  # в черновом варианте - просто оформление заказа
    steps.choose_item(user_no_card)
    order_number = steps.submit_and_pay(user_no_card)
    steps.buyout_and_status_change(driver, order_number, "AB")


@allure.issue("https://jira.pochtavip.com/secure/Tests.jspa#/testCase/LGC-T2341", "LGC-T2341")
@allure.feature("Оформлен")
@allure.story('Тест: "Оформлен" без баллов, с картой, оплата наличными при получении')
@pytest.mark.with_card
@pytest.mark.processed
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
def test_partial_cancelled_pay_cash_no_bonus_card(user_no_card, driver):
    steps.choose_two_items(user_no_card)
    order_number = steps.submit_and_pay(user_no_card)
    steps.buyout_and_status_change(driver, order_number, "OI")


@allure.issue("https://jira.pochtavip.com/secure/Tests.jspa#/testCase/LGC-T2339", "LGC-T2339")
@allure.feature("Частичный отказ")
@allure.story('Тест: "Частичный отказ" без баллов, с картой, оплата наличными при получении')
@pytest.mark.with_card
@pytest.mark.partial_cancelled
def test_partial_cancelled_no_bonus_pay_cash_with_bonus_card(user_with_card, driver):
    steps.choose_two_items(user_with_card)
    order_number = steps.submit_and_pay(user_with_card)
    steps.buyout_and_status_change(driver, order_number, "OI")
    history_page = steps.loymax_ops(driver, user_with_card)
    steps.asserts_partial_cancelled_no_bonus_have_card(history_page, order_number)


@allure.issue("https://jira.pochtavip.com/secure/Tests.jspa#/testCase/LGC-T2340", "LGC-T2340")
@allure.feature("Частичный отказ")
@allure.story('Тест: "Частичный отказ" со списанием бонусов, с картой, оплата наличными при получении')
@pytest.mark.with_card
@pytest.mark.partial_cancelled
def test_partial_cancelled_with_bonus_pay_cash(user_with_card, driver):
    steps.choose_two_items(user_with_card)
    order_number = steps.submit_and_pay(user_with_card, bonuses=True)
    steps.buyout_and_status_change(driver, order_number, "OI")
    history_page = steps.loymax_ops(driver, user_with_card)
    steps.asserts_partial_cancelled_pay_bonus_have_card(history_page, order_number)

