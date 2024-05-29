import re
import time

from pages.utils import LOAD_TIMEOUT, ACCOUNT_URL
from pages.base_page import BasePage


class AccountPage(BasePage):
    url = ACCOUNT_URL

    def make_deposit(self, amount):
        self.make_transaction(amount, "Deposit")

    def make_withdrawl(self, amount):
        self.make_transaction(amount, "Withdrawl")

    def check_success_message(self, msg):
        success_msg = self.search_by_xpath('//span[contains(text(), "{}")]'.format(msg))
        return success_msg is not None

    def make_transaction(self, amount, transaction_type="Deposit"):
        self.click_button(transaction_type)
        time.sleep(0.5)
        input = self.choose_input("amount")
        self.input_text(input, amount)

        xpath = '//button[@type="submit" and contains(text(), "{}")]'.format(
            transaction_type if transaction_type == "Deposit" else "Withdraw")
        self.click_button(transaction_type if transaction_type == "Deposit" else "Withdraw", xpath)

    def get_balance(self):
        price = self.search_by_xpath("//div[@ng-hide='noAccount']")
        res = re.findall(r'Balance : \d+', price.text)
        if len(res):
            res = re.findall(r'\d+', res[0])
            return int(res[0]) if len(res) else None

    def choose_transaction(self):
        self.click_button("Transactions")