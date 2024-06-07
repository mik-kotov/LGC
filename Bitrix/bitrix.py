from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Front_base import locators_front, browser_works
import API.order_submit
import time
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By

class Bitrix:

def check_authorization(browser):
    browser.implicitly_wait(10)
    if len(browser.find_elements(By.CSS_SELECTOR, ".bx-admin-auth-form")) > 0:
        login_input_field = browser.find_element(By.XPATH, '//input[@name="USER_LOGIN"][@tabindex="1"]')
        password_input_field = browser.find_element(By.XPATH, '//input[@tabindex="2"]')
        confirm_button = browser.find_element(By.CSS_SELECTOR, '.login-btn-green[tabindex = "4"]')
        login_input_field.clear()
        login_input_field.send_keys("lgcity\Mikhail.Kotov")
        password_input_field.send_keys("QLEp38z5_6)7")
        confirm_button.click()
        return browser


def bitrix_ops(current_link):

    browser = browser_works.browser
    browser.implicitly_wait(10)
    browser_works.start_work(browser, current_link)
    check_authorization(browser)
    return browser


def order_link(order_id):

    return locators_front.BITRIX_ORDER_CARD_LINK + str(order_id)


def order_edit_link(order_id):

    return locators_front.BITRIX_ORDER_EDIT_LINK + str(order_id)


def order_status_change(browser, order_status):
    browser.implicitly_wait(10)
    select = Select(browser.find_element(By.CSS_SELECTOR, "#STATUS_ID"))
    select.select_by_value(order_status)
    save_status_button = browser.find_element(By.CSS_SELECTOR, "#save_status_button")
    save_status_button.click()
    print(f"Статус товара изменен на {order_status}")


def change_buyout_status_to_yes(browser):
    change_item_popup_logo = browser.find_element(By.XPATH,
                                                  "//table[@id='sale_order_basketsale_order_edit_product_table']/tbody[3]/descendant::span[@class='adm-s-order-item-title-icon']")
    browser.execute_script("arguments[0].scrollIntoView(true);", change_item_popup_logo)
    change_item_popup = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH,
                                                                                           "//table[@id='sale_order_basketsale_order_edit_product_table']/tbody[3]/descendant::span[@class='adm-s-order-item-title-icon']")))
    browser.execute_script("arguments[0].click();", change_item_popup)
    change_item_button = browser.find_element(By.CSS_SELECTOR, ".bx-core-popup-menu-item-text")
    change_item_button.click()
    browser.find_element(By.XPATH,
                         "//div[@id='bx-admin-prefix']//input[@value='Выкуплен']/../self::td/following-sibling::td/input[@value='Нет']").clear()
    browser.find_element(By.XPATH,
                         "//div[@id='bx-admin-prefix']//input[@value='Выкуплен']/../self::td/following-sibling::td/input[@value='Нет']").send_keys("Да")
    change_item_save_button = browser.find_element(By.CSS_SELECTOR, "#save_custom_product")
    change_item_save_button.click()
    save_order_changes_button = browser.find_element(By.CSS_SELECTOR, '.adm-detail-content-btns .adm-btn-save')
    save_order_changes_button.click()
    print('Товар выкуплен')



