from API import data
from API.authorization import APIClient
from API.order import Order
from selenium import webdriver
import allure
import pytest
import time

def prepare_user(user):
    with allure.step("Подготовка пользователя"):
        start_order = Order(user)
        with allure.step("Очищаем корзину"):
            start_order.reset_order()
        with allure.step("Очищаем заказ"):
            start_order.reset_cart()

@pytest.fixture(scope='session')
def driver():
    print("")
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    #options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)

    yield driver
    time.sleep(1.5)
    allure.attach(driver.get_screenshot_as_png(), name="Скриншот перед закрытием теста",
                  attachment_type=allure.attachment_type.PNG)
    driver.quit()

@pytest.fixture(scope="function")
def user_no_card():
    user = data.get_random_user_with_no_card()
    user_no_card = APIClient(user)
    with allure.step(f"Пользователь {user}"):
        prepare_user(user_no_card)
        return user_no_card

@pytest.fixture(scope="function")
def user_with_card():
    user_and_card = data.get_random_user_with_card()
    card = user_and_card[1]
    user = user_and_card[0]
    user_with_card = APIClient(user, card)
    with allure.step(f"Пользователь: {user}, карта: {card}"):
        prepare_user(user_with_card)
        return user_with_card

