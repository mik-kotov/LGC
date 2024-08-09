from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Front_base.locators_front import LoyalLocators
from selenium.webdriver.support.ui import Select

import allure
import time


def retry(max_attempts, delay=1):
    def decorator(func):
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    print(f"Attempt {attempts} failed: {e}")
                    time.sleep(delay)
            raise RuntimeError(f"Function {func.__name__} failed after {max_attempts} attempts")
        return wrapper
    return decorator


class Browser:

    def __init__(self, browser, order=None):
        self.browser = browser
        self.order = order
        self.browser.implicitly_wait(10)

    def open(self, link):

        self.browser.get(link)

    def click(self, locator):
        allure.attach(self.browser.get_screenshot_as_png(),
                      name='Скриншот перед кликом', attachment_type=allure.attachment_type.PNG)
        locator.click()

    def find_element(self, how, what, timeout=10):

        element = WebDriverWait(self.browser, timeout).until(
            EC.presence_of_element_located((how, what))
        )
        return element


    def find_elements(self, how, what):

        return self.browser.find_elements(how, what)

    def scroll_into_view(self, element):

        return self.browser.execute_script('arguments[0].scrollIntoView({block: "center"});',
                                           element)

    def is_element_present(self, how, what, timeout=4):
        try:
            WebDriverWait(self.browser, timeout).until(EC.presence_of_element_located((how, what)))
        except TimeoutException:
            return False
        return True

    def is_not_element_present(self, how, what, timeout=4):
        try:
            WebDriverWait(self.browser, timeout).until(EC.presence_of_element_located((how, what)))
        except TimeoutException:
            return True

        return False

    def wait_for_url(self, expected_url, timeout=10):
        WebDriverWait(self.browser, timeout).until(
            lambda driver: driver.current_url == expected_url
        )
