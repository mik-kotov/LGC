import browser_works
import bitrix_locators
from API import  choose_item_in_catalog
from API import configuration
from API import order_submit
import time
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
import functools


def go_to_bitrix():
    current_link = bitrix_locators.BITRIX_MAIN_PAGE
    browser = browser_works.start_work(browser_works.browser, current_link)
    input("Press Enter to continue...")
    browser.quit()
    time.sleep(60)

def check_authorization(browser):

    browser.implicitly_wait(10)
    if len(browser.find_elements(By.CSS_SELECTOR, ".bx-admin-auth-form")) > 0:
        login_input_field = browser.find_element(By.XPATH, '//input[@name="USER_LOGIN"][@tabindex="1"]')
        password_input_field = browser.find_element(By.XPATH, '//input[@tabindex="2"]')
        confirm_button = browser.find_element(By.CSS_SELECTOR, '.login-btn-green[tabindex = "4"]')
        login_input_field.clear()
        login_input_field.send_keys("lgcity\Mikhail.Kotov")
        password_input_field.send_keys("Aboba1337")
        confirm_button.click()
        return browser
def go_to_order(order_id):
    current_link = bitrix_locators.BITRIX_ORDER_CARD_LINK + str(order_id)
    print(current_link)
    browser = browser_works.browser
    browser.implicitly_wait(10)
    browser_works.start_work(browser, current_link)
    check_authorization(browser)
    return browser

def order_status_change(order_id, order_status):
    print(order_id)
    browser = go_to_order(order_id)
    browser.implicitly_wait(10)
    select = Select(browser.find_element(By.CSS_SELECTOR, "#STATUS_ID"))
    select.select_by_value(order_status)
    save_status_button = browser.find_element(By.CSS_SELECTOR, "#save_status_button")
    save_status_button.click()


current_order_id = order_submit.add_item_and_order_submit()
order_status_change(current_order_id,"NI")