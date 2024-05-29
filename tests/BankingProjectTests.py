import datetime
import csv
import pytest
from sympy import fibonacci
import configparser

from allure_commons.types import AttachmentType
import allure

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions

from pages.login_page import LoginPage
from pages.account_page import AccountPage
from pages.customer_page import CustomerPage
from pages.list_tx_page import ListTxPage


def custom_fib(num):
    if num == 1 or num == 2:
        return 1
    return custom_fib(num - 1) + custom_fib(num - 2)


def format_transactions_data(transactions):
    for tran in transactions:
        trans_time = tran[0].replace(",", "").split(" ")
        t = datetime.datetime.strptime(" ".join([trans_time[-2], trans_time[-1]]), '%I:%M:%S %p')
        time_ = t.strftime('%H:%M:%S')
        tran[0] = " ".join([trans_time[1], trans_time[0], trans_time[2], time_])
        assert tran[2] in ("Credit", "Debit")


def gen_csv(csv_name, transactions):
    with open(csv_name, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerows(transactions)


class TestBankingProject:
    @classmethod
    def setup_class(cls):
        cls.config = configparser.ConfigParser()
        cls.config.read("config.ini")
        cls.node_url = cls.config["TestCapabilities"]["node_url"]
        cls.browser_name = cls.config["TestCapabilities"]["browser_name"]
        cls.csv_file_path = cls.config["TestCapabilities"]["transaction_file_name"]
        cls.login_name = cls.config["TestCapabilities"]["login_name"]

        browsers = ["chrome", "firefox", "edge"]
        if cls.browser_name not in browsers:
            raise ValueError("{} not in {}".format(cls.browser_name, browsers))

        if cls.browser_name == "chrome":
            options = ChromeOptions()
        elif cls.browser_name == "firefox":
            options = FirefoxOptions()
        else:
            options = EdgeOptions()


        cls.driver = webdriver.Remote(command_executor=cls.node_url,
                                      options=options)
        cls.driver.maximize_window()
        now = datetime.datetime.now()
        number = now.day + 1
        cls.fib_num = custom_fib(number)

    @classmethod
    def teardown_class(cls):
        if cls.driver is not None:
            cls.driver.close()

    @pytest.mark.order(1)
    def test_login(self):
        allure.title("Test addition of two numbers")
        login_page = LoginPage(self.driver)
        login_page.get_page()
        assert login_page.check_page(), "Url doesn't match {}".format(login_page.url)
        login_page.login("Customer Login")

        customer_page = CustomerPage(self.driver)
        assert customer_page.check_page(), "Url doesn't match {}".format(customer_page.url)
        customer_page.choose_login(self.login_name)

        account_page = AccountPage(self.driver)
        login_name = account_page.search_by_xpath('//span[contains(text(), "{}")]'.format((self.login_name)))
        assert login_name is not None, "Cannot find login name in page"

    @pytest.mark.order(2)
    def test_fibonachi(self):
        now = datetime.datetime.now()
        number = now.day + 1
        assert fibonacci(number) == custom_fib(number)

    @pytest.mark.order(3)
    def test_deposit(self):
        account_page = AccountPage(self.driver)
        assert account_page.check_page(), "Url doesn't match {}".format(account_page.url)
        account_page.make_deposit(self.fib_num)
        assert account_page.check_success_message("Deposit Successful"), "No message `Deposit successful`"

    @pytest.mark.order(4)
    def test_withdraw(self):
        account_page = AccountPage(self.driver)
        assert account_page.check_page(), "Url doesn't match {}".format(account_page.url)
        account_page.make_withdrawl(self.fib_num)
        assert account_page.check_success_message("Transaction successful"), "No message `Transaction successful`"

    @pytest.mark.order(5)
    def test_check_balance(self):
        account_page = AccountPage(self.driver)
        assert account_page.check_page(), "Url doesn't match {}".format(account_page.url)
        balance = account_page.get_balance()
        assert balance == 0, "Balance must be equal zero"

    @pytest.mark.order(6)
    def test_check_transaction(self):
        account_page = AccountPage(self.driver)
        assert account_page.check_page(), "Url doesn't match {}".format(account_page.url)
        account_page.choose_transaction()

        list_tx_page = ListTxPage(self.driver)
        list_tx_page.get_page()
        assert list_tx_page.check_page(), "Url doesn't match {}".format(list_tx_page.url)
        transactions = list_tx_page.load_transactions()

        found_deposit = False
        found_withdraw = False

        for trans in transactions:
            if "Credit" in trans and str(self.fib_num) in trans:
                found_deposit = True
            if "Debit" in trans and str(self.fib_num) in trans:
                found_withdraw = True
        assert found_deposit, "No deposit found"
        assert found_withdraw, "No withdraw found"
        format_transactions_data(transactions)
        gen_csv(self.csv_file_path, transactions)
        allure.attach.file(self.csv_file_path, name="Attached CSV File", attachment_type=AttachmentType.CSV)

