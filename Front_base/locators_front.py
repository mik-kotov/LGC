from selenium.webdriver.common.by import By




class BasePageLocators:

    LOGIN_LINK_FROM_HEADER = (By.XPATH, "(//a[contains(@class, 'header__login-link')])[1]")
    PROFILE_ICON_LINK_FROM_HEADER = (By.XPATH, "(//html/body/div[@id='barba-wrapper']/div/header[1]/div[2]/div/div[@class='header__right-side']/a])")
    GO_TO_ADMIN_BITRIX = (By.CSS_SELECTOR,"#bx-panel-admin-tab")


class LoginPageLocators:

    LOGIN_BY_PASSWORD_LINK = (By.CSS_SELECTOR, ".phone_login > .js-toggle-pass-login")
    LOGIN_BY_PASSWORD_EMAIL_INPUT_FIELD = (By.CSS_SELECTOR, "[name = 'log_email']")
    LOGIN_BY_PASSWORD_PASSWORD_INPUT_FIELD = (By.CSS_SELECTOR, "[name = 'log_pass']")


class BitrixLocators:

    BASIC_LOGIN_AND_PASSWORD_IN_LINK = "devel:lgdevpass@"
    AUTHORIZATION_PAGE = f"https://{BASIC_LOGIN_AND_PASSWORD_IN_LINK}app-monolith.mylgc.ru/bitrix/admin/sale_order.php?lang=ru#authorize"
    LOGIN_FIELD = (By.XPATH, '//input[@name="USER_LOGIN"][@tabindex="1"]')
    PASSWORD_FIELD = (By.XPATH, '//input[@tabindex="2"]')
    CONFIRM_BUTTON = (By.CSS_SELECTOR, '.login-btn-green[tabindex = "4"]')
    LOGIN = "lgcity\\Mikhail.Kotov"
    PASSWORD = "QLEp38z5_6)7"
    STATUS_SELECTOR = (By.CSS_SELECTOR, "#STATUS_ID")
    SAVE_STATUS_BUTTON = (By.CSS_SELECTOR, "#save_status_button")
    CHANGE_ITEM_POPUP_LOGO = (By.XPATH, "//table[@id='sale_order_basketsale_order_edit_product_table']/tbody[3]/descendant::span[@class='adm-s-order-item-title-icon']")
    CHANGE_ITEM_POPUP = (By.XPATH, "//table[@id='sale_order_basketsale_order_edit_product_table']/tbody[3]/descendant::span[@class='adm-s-order-item-title-icon']")
    CHANGE_ITEM_BUTTON = (By.CSS_SELECTOR, ".bx-core-popup-menu-item-text")
    CHANGE_ITEM_SAVE_BUTTON = (By.CSS_SELECTOR, "#save_custom_product")
    SAVE_ORDER_CHANGES_BUTTON = (By.CSS_SELECTOR, '.adm-detail-content-btns .adm-btn-save')

    MAIN_PAGE = "https://app-monolith.mylgc.ru/bitrix/admin/sale_order.php?lang=ru"
    ORDER_CARD_LINK = f"https://app-monolith.mylgc.ru/bitrix/admin/sale_order_view.php?amp%3Bfilter=Y&%3Bset_filter=Y&lang=ru&ID=" ## + order_id
    ORDER_EDIT_LINK = f"https://app-monolith.mylgc.ru/bitrix/admin/sale_order_edit.php?ID=" ## + order_id



class LoyalLocators:

    LOGIN_INPUT = (By.CSS_SELECTOR, "#LoginForm_login")
    PASSWORD_INPUT = (By.CSS_SELECTOR, "#LoginForm_password")
    AUTHORIZATION_BUTTON = (By.XPATH, "//button[@tabindex='0']")
    SEARCH_USER_BUTTON = (By.CSS_SELECTOR, "#searchByAttributesButton")
    SEARCH_USER_FRAME = (By.CSS_SELECTOR, "#armIframe")
    SEARCH_USER_PHONE_INPUT = (By.CSS_SELECTOR, ".cy-phone")
    SEARCH_USER_BY_PHONE_BUTTON = (By.CSS_SELECTOR, ".btn-primary[type='submit']")
    USER_PURCHASES_BUTTON = (By.CSS_SELECTOR, "#purchaseHistory")
    USER_PERSONAL_INFO_BUTTON = (By.CSS_SELECTOR,"#personalInfo")
    USER_PURCHASES_TABLE = (By.XPATH, "//purchases//tbody")
    USER_PURCHASES_ORDER_NUMBER = (By.XPATH, "//purchases//tbody/tr[1]/td[3]")
    USER_PURCHASES_STATUS_CONFIRMED = (By.XPATH, '//purchases//tbody/tr[1]/td/div[@class="b-icon-progress b-icon-state--confirmed"]')

