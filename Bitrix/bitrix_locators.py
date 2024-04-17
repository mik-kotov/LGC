from selenium.webdriver.common.by import By

BASIC_LOGIN_AND_PASSWORD_IN_LINK = "devel:lgdevpass@"
class BasePageLocators():

    LOGIN_LINK_FROM_HEADER = (By.XPATH, "(//a[contains(@class, 'header__login-link')])[1]")
    PROFILE_ICON_LINK_FROM_HEADER = (By.XPATH, "(//html/body/div[@id='barba-wrapper']/div/header[1]/div[2]/div/div[@class='header__right-side']/a])")
    GO_TO_ADMIN_BITRIX = (By.CSS_SELECTOR,"#bx-panel-admin-tab")
class LoginPageLocators():

    LOGIN_BY_PASSWORD_LINK = (By.CSS_SELECTOR, ".phone_login > .js-toggle-pass-login")
    LOGIN_BY_PASSWORD_EMAIL_INPUT_FIELD = (By.CSS_SELECTOR, "[name = 'log_email']")
    LOGIN_BY_PASSWORD_PASSWORD_INPUT_FIELD = (By.CSS_SELECTOR, "[name = 'log_pass']")

BITRIX_MAIN_PAGE = f"https://{BASIC_LOGIN_AND_PASSWORD_IN_LINK}app-monolith.mylgc.ru/bitrix/admin/sale_order.php?lang=ru"

BITRIX_ORDER_CARD_LINK = f"https://{BASIC_LOGIN_AND_PASSWORD_IN_LINK}app-monolith.mylgc.ru/bitrix/admin/sale_order_view.php?amp%3Bfilter=Y&%3Bset_filter=Y&lang=ru&ID=" ## + order_id
