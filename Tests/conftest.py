import pytest
from API import data
from API.authorization import APIClient
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
import pytest
from API import authorization, choose_item_in_catalog, order_submit
from Bitrix.bitrix import Bitrix
from Front_base.browser_works import Browser
from Loymax import login_page, user_page, call_center
from Loymax.base_page import LoymaxBasePage
from Loymax.login_page import LoymaxLoginPage

chrome_driver_path = r'C:\chromedriver\chromedriver.exe'
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("--headless")
service = Service(chrome_driver_path)
browser = webdriver.Chrome(service=service, options=options)


@pytest.yield_fixture(scope='session')
def browser():
    print("")
    chrome_driver_path = r'C:\chromedriver\chromedriver.exe'
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    #options.add_argument("--headless")
    service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=options)
    yield driver
    driver.quit()

@pytest.fixture(scope="function")
def user_no_card():
    user = data.user_no_card_phone
    user_no_card = APIClient(user)
    return user_no_card

@pytest.fixture(scope="function")
def user_with_card():
    user = data.user_with_card_phone
    card = data.user_card
    user_with_card = APIClient(user, card)
    print(user)
    return user_with_card

