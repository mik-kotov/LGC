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

    AUTHORIZATION_WINDOW = (By.CSS_SELECTOR, "#popup_alignment")
    BASIC_LOGIN_AND_PASSWORD_IN_LINK = "devel:lgdevpass@"
    AUTHORIZATION_PAGE = f"https://{BASIC_LOGIN_AND_PASSWORD_IN_LINK}app-monolith.mylgc.ru/bitrix/admin/sale_order.php?lang=ru#authorize"
    LOGIN_FIELD = (By.XPATH, '//input[@name="USER_LOGIN"][@tabindex="1"]')
    PASSWORD_FIELD = (By.XPATH, '//input[@tabindex="2"]')
    CONFIRM_BUTTON = (By.CSS_SELECTOR, '.login-btn-green[tabindex = "4"]')
    LOGIN = "lgcity\\Mikhail.Kotov"
    PASSWORD = "QLEp38z5_6)7"
    GO_TO_ORDER_FROM_CHANGE_ORDER_PAGE_BUTTON = (By.CSS_SELECTOR, '[title="Перейти к просмотру заказа"]')
    STATUS_SELECTOR = (By.CSS_SELECTOR, "#STATUS_ID")
    SAVE_STATUS_BUTTON = (By.CSS_SELECTOR, "#save_status_button")
    CHANGE_ITEM_POPUP_B = (By.CSS_SELECTOR, ".adm-s-order-item-title-icon")
    CHANGE_ITEM_POPUP = (By.XPATH, '//table//tbody[3]//span[@class="adm-s-order-item-title-icon"]')
    CHANGE_ITEM_BUTTON = (By.CSS_SELECTOR, ".bx-core-popup-menu-item-text")
    CHANGE_PAY_POPUP = (By.CSS_SELECTOR, "#BUTTON_PAID_0_SHORT")
    CHANGE_PAY_TO_YES_BUTTON = (By.CSS_SELECTOR, '.bx-core-popup-menu-item')
    CHANGE_PAY_SAVE_BUTTON = (By.CSS_SELECTOR, '[name="undefined"]#undefined') #кринж
    CHANGE_ITEM_SAVE_BUTTON = (By.CSS_SELECTOR, "#save_custom_product")
    SAVE_ORDER_CHANGES_BUTTON = (By.CSS_SELECTOR, '.adm-detail-content-btns .adm-btn-save')
    PURCHASED_INPUT_A = (By.CSS_SELECTOR, "[id*=_VALUE_10]")
    PURCHASED_INPUT_B = (By.XPATH, "//div[@id='bx-admin-prefix']//input[@value='Выкуплен']/../self::td/following-sibling::td/input[@value='Нет']")
    PROMOCODE_FIELD = (By.XPATH, "//*[.='Купон:']")
    PROMOCODE_NAME = (By.XPATH, "//*[.='Купон:']/following-sibling::td/div")
    ORDER_PRICE = (By.CSS_SELECTOR, "#sale-order-financeinfo-price-view")
    FIRST_ITEM_FINAL_PRICE = (By.XPATH, '//table[@id="sale_order_basketsale_order_view_product_table"]/tbody[3]/tr[1]//strong[1]')


    MAIN_PAGE = "https://app-monolith.mylgc.ru/bitrix/admin/sale_order.php?lang=ru"
    ORDER_CARD_LINK = f"https://app-monolith.mylgc.ru/bitrix/admin/sale_order_view.php?amp%3Bfilter=Y&%3Bset_filter=Y&lang=ru&ID=" ## + order_id
    ORDER_EDIT_LINK = f"https://app-monolith.mylgc.ru/bitrix/admin/sale_order_edit.php?ID=" ## + order_id


class LoyalLocators:

    IS_AUTHORIZED_SIGN = (By.CSS_SELECTOR, ".menu-link.active")
    LOGIN_INPUT = (By.CSS_SELECTOR, "#LoginForm_login")
    PASSWORD_INPUT = (By.CSS_SELECTOR, "#LoginForm_password")
    AUTHORIZATION_BUTTON = (By.XPATH, "//button[@tabindex='0']")
    CONTACT_CENTER_BUTTON = (By.XPATH, "//a[.='Контакт-центр'][@class='menu-link']")
    SEARCH_USER_BUTTON = (By.CSS_SELECTOR, "#searchByAttributesButton")
    SEARCH_USER_FRAME = (By.CSS_SELECTOR, "#armIframe")
    SEARCH_USER_PHONE_INPUT = (By.XPATH, '//input[@placeholder="- Номер телефона -"]')
    SEARCH_USER_BY_PHONE_BUTTON = (By.CSS_SELECTOR, ".btn-primary[type='submit']")
    USER_PURCHASES_BUTTON = (By.CSS_SELECTOR, "#purchaseHistory")
    USER_PERSONAL_INFO_BUTTON = (By.CSS_SELECTOR, "#personalInfo")
    USER_PURCHASES_TABLE = (By.XPATH, "//purchases//tbody")
    USER_PURCHASES_ORDER_NUMBER = (By.XPATH, "//purchases//tbody/tr[1]/td[3]")
    USER_PURCHASES_STATUS_CONFIRMED = (By.XPATH, '//purchases//tbody/tr[1]//div[@title="Подтверждена"]')
    USER_PURCHASES_STATUS_CANCELLED = (By.XPATH, '//purchases//tbody/tr[1]//div[@title="Отменена"]')
    USER_PURCHASES_STATUS_CREATED = (By.XPATH, '//purchases//tbody/tr[1]//div[@title="Создана"]')
    FIRST_FROM_TOP_PURCHASE_NUMBER = (By.XPATH, "//purchases//tbody/tr[1]/td[3]")
    SECOND_FROM_TOP_PURCHASE_LOUPE = (By.XPATH, '//purchases//tbody/tr[2]//button')
    SECOND_FROM_TOP_PURCHASE_NUMBER = (By.XPATH, "//purchases//tbody/tr[2]/td[3]")
    SECOND_FROM_TOP_PURCHASE_CANCELLED = (By.XPATH, "//purchases//tbody/tr[2]//div[@title='Отменена']")
    USER_PURCHASE_LOUPE = (By.XPATH, "//purchases//tbody/tr[1]//button")
    TEXT_ADDED_BONUS = (By.XPATH, "//*[.=' Бонус ']")
    ADDED_BONUSES_COUNT = (By.XPATH, "//*[.=' Бонус ']/following-sibling::td[1]/div/span")
    ADDED_BONUS_CONFIRMED = (By.XPATH, "//*[.=' Бонус ']/following-sibling::td[2]/div[@title='Подтверждена']")
    ADDED_BONUS_CANCELLED = (By.XPATH, '//*[.=" Бонус "]/following-sibling::td[2]/div[@title="Отменена"]')
    PAID_BONUS_CONFIRMED = (By.XPATH, "//*[.=' Оплата ']/following-sibling::td[2]/div[@title='Подтверждена']")
    PAID_BONUS_CANCELLED = (By.XPATH, "//*[.=' Оплата ']/following-sibling::td[2]/div[@title='Отменена']")
    PAID_BONUSES_COUNT = (By.XPATH, "//*[.=' Оплата ']/following-sibling::td[1]/div/span")
    USED_PROMOCODE = (By.CSS_SELECTOR, '[ng-repeat="number in purchase.couponNumbers"]')
    LOYMAX_ORDER_SUM = (By.XPATH, '//td[.="По чеку:"]/following-sibling::td[4]/b')
    BUTTON_BACK_TO_HISTORY = (By.CSS_SELECTOR, '[class="b-link b-text--info"]')

    ACCRUAL_RADIOBUTTON = (By.CSS_SELECTOR, '[title="Начисление"]')
    SELECT_COMPANY_LIST = (By.CSS_SELECTOR, '._open .b-list__selected')
    OOO_TRADE_MANAGEMENT = (By.XPATH, '//div[@class="cy-item b-list__item"][6]')

                                 #select_element = self.find_element(*BitrixLocators.STATUS_SELECTOR)
                                 #select = Select(select_element)
                                 #select.select_by_value(order_status)

    CURRENCIES_LIST = (By.CSS_SELECTOR, '#currency .b-list__selected')
    CHOOSE_BONUSES_AS_CURRENCY = (By.XPATH, '//div[@class="cy-item b-list__item"][1]')
    DESCRIPTION_FIELD = (By.CSS_SELECTOR, '#description')
    INTERNAL_DESCRIPTION_FIELD = (By.CSS_SELECTOR, '#internalDescription')
    CHOOSE_ID = (By.CSS_SELECTOR, '[translationtable = "identifierType"]')
    CHOOSE_CARD_AS_ID = (By.CSS_SELECTOR, '[title="Номер карты"]')
    ID_INPUT_FIELD = (By.CSS_SELECTOR, '#item_card_0')
    AMOUNT_BONUS_FIELD = (By.CSS_SELECTOR, "#item_amount_0")
    OPERATION_DETAILS_FIELD = (By.CSS_SELECTOR, '#item_DetailDescription_0')
    APPLY_BUTTON = (By.XPATH, '//*[@class="b-btn b-btn--success"]')

    SUCSESS_TEXT = (By.XPATH, '//span[.=" Обработана "]')
