from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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

    def get_screenshot(self, name='Скриншот'):
        allure.attach(self.browser.get_screenshot_as_png(),
                      name, attachment_type=allure.attachment_type.PNG)
    def click(self, locator):
        self.get_screenshot('Скриншот перед кликом')
        locator.click()

    def click_js(self, element):
        self.get_screenshot('Скриншот перед кликом')
        self.browser.execute_script("arguments[0].click();", element)

    def scroll_to_element_centered(self, element):
        self.browser.execute_script(
            'arguments[0].scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"})', element)

    def scroll_to_bottom(self):
        self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight)")
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
