import time

from selenium.webdriver.common.by import By

from pages.utils import LIST_TX_URL
from pages.base_page import BasePage
from pages.account_page import AccountPage


class ListTxPage(BasePage):
    url = LIST_TX_URL

    def load_transactions(self):
        rows = []

        table_element = self.search_by_xpath('(//table)[1]')
        length = len(table_element.find_elements(By.TAG_NAME, 'tr'))

        if length == 1:
            account_page = AccountPage(self.driver)
            account_page.get_page()
            time.sleep(2)
            self.get_page()
            assert self.check_page()

        table_element = self.search_by_xpath('(//table)[1]')
        length = len(table_element.find_elements(By.TAG_NAME, 'tr'))
        for i in range(length + 1):
            for row in table_element.find_elements(By.ID, 'anchor{}'.format(i)):
                cells = [cell.text for cell in row.find_elements(By.TAG_NAME, 'td')]
                rows.append(cells)

        return rows
