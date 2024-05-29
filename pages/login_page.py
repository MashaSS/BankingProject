from pages.utils import LOAD_TIMEOUT, LOGIN_URL
from pages.base_page import BasePage


class LoginPage(BasePage):
    url = LOGIN_URL

    def login(self, login_type="Customer Login"):
        self.click_button(login_type)