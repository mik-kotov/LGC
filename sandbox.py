from selenium import webdriver

from selenium.webdriver.chrome.service import Service
import time
from pages import locators

//*[text()="№1024234"] #не нужен. Заменяется на https://app-monolith.mylgc.ru/bitrix/admin/sale_order_view.php?amp%3Bfilter=Y&%3Bset_filter=Y&lang=ru&ID=1024233
select = Select(driver.find_element_by_id(By.CSS_SELECTOR, "#STATUS_ID"))
#select.select_by_value("NI")
