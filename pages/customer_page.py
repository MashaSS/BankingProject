from selenium.webdriver.support.ui import Select

from pages.utils import CUSTOMER_URL
from pages.base_page import BasePage


class CustomerPage(BasePage):
    url = CUSTOMER_URL

    def choose_login(self, name):
        user_select = self.search_by_id('userSelect')
        user_select.click()

        user_select_ = Select(user_select)
        user_select_.select_by_visible_text(name)
        user_select.click()

        self.click_button("Login")

