from API import data
from API.authorization import APIClient
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from Tests import test_loyalty
import allure
import pytest

chrome_driver_path = r'C:\chromedriver\chromedriver.exe'
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("--headless")
service = Service(chrome_driver_path)
browser = webdriver.Chrome(service=service, options=options)


@pytest.fixture(scope='session')
def driver():
    print("")
    chrome_driver_path = r'C:\chromedriver\chromedriver.exe'
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    # options.add_argument("--headless")
    service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=options)

    yield driver

    allure.attach(driver.get_screenshot_as_png(), name="Скриншот перед закрытием теста",
                  attachment_type=allure.attachment_type.PNG)
    driver.quit()

@pytest.fixture(scope="function")
def user_no_card():
    user = data.get_random_user_with_no_card()
    user_no_card = APIClient(user)
    return user_no_card

@pytest.fixture(scope="function")
def user_with_card():
    user_and_card = data.get_random_user_with_card()
    user_with_card = APIClient(user_and_card[0], user_and_card[1])
    return user_with_card

