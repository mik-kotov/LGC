from front_base.browser_works import Browser


class BitrixBasePage(Browser):

    def go_to_main_page(self):
        self.open('https://app-monolith.mylgc.ru/bitrix/admin/sale_order.php')

