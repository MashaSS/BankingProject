from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pages.utils import LOAD_TIMEOUT


class BasePage():
    def __init__(self, driver):
        self.driver = driver

    def get_page(self, time=LOAD_TIMEOUT):
        if self.url is not None:
            self.driver.get(self.url)
            wait = WebDriverWait(self.driver, time)
            wait.until(lambda driver: self.driver.execute_script('return document.readyState') == 'complete')

    def check_page(self):
        loaded = False
        try:
            wait = WebDriverWait(self.driver, 1)
            wait.until( lambda driver: self.driver.current_url == self.url)
            loaded = True
        except TimeoutError:
            print("Cannot load page!")
        finally:
            return loaded

    def click_button(self, text, xpath=None):
        if xpath is None:
            xpath = '//button[contains(text(), "{}")]'.format(text)
        button = self.search_by_xpath(xpath)
        button.click()

    def choose_input(self, text):
        input = self.search_by_xpath('//input[@placeholder="{}"]'.format(text))
        input.click()
        return input

    def input_text(self, input, input_text):
        input.clear()
        input.send_keys(str(input_text))

    def search_by_id(self, name, time=LOAD_TIMEOUT):
        element_present = EC.visibility_of_element_located((By.ID, name))
        return self.find_element(element_present)

    def search_by_xpath(self, xpath):
        element_present = EC.visibility_of_element_located(
            (By.XPATH, xpath))
        return self.find_element(element_present)

    def find_element(self, element_present):
        found_element = None
        try:
            found_element = WebDriverWait(self.driver, LOAD_TIMEOUT).until(element_present)
        except TimeoutError:
            print("Cannot find element!")
        finally:
            return found_element