from Front_base.browser_works import Browser
from Front_base.locators_front import LoyalLocators

class LoymaxBasePage(Browser):

    def go_to_call_center_page_from_main_page(self):
        link = "https://lgcity-pstg.loymax.tech/#/home"
        self.open(link)
        call_center_button = self.find_element(*LoyalLocators.CONTACT_CENTER_BUTTON)
        self.click(call_center_button)

    def go_to_login_page(self):
        link = "https://lgcity-pstg.loymax.tech/#/login"
        self.open(link)





