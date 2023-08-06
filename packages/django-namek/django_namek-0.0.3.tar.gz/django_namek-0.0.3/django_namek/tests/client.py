import time
import random
import logging
from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from django_namek import constants

logger = logging.getLogger('django_namek')


"""

Definition of `By` method :

- ID
- XPATH
- LINK_TEXT
- PARTIAL_LINK_TEXT
- NAME
- TAG_NAME
- CLASS_NAME
- CSS_SELECTOR

"""


class Client(webdriver.Chrome):
    timeout = 10
    time_wait_min = None
    time_wait_max = None
    open_browser = constants.DN_TEST_BROWSER_OPEN

    def __init__(self, *args, **kwargs):
        if not self.open_browser:
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('--headless')
            with Display(visible=0, size=(800, 600)):
                super().__init__(
                    chrome_options=chrome_options,
                    *args, **kwargs
                )
        else:
            self.time_wait_min = 0.1
            self.time_wait_max = 0.2
            super().__init__(*args, **kwargs)

    def wait(self):
        if self.time_wait_min and self.time_wait_max:
            ms = random.uniform(self.time_wait_min, self.time_wait_max)
            logger.info('Wait %s secondes' % str(round(ms, 2)))
            time.sleep(ms)

    def stop_driver(self):
        self.delete_all_cookies()
        self.quit()

    def get(self, url):
        super().get(url)
        logger.info('GET ' + url)
        self.wait()

    def input_query(self, input_name, query):
        try:
            WebDriverWait(super(), self.timeout).until(
                EC.element_to_be_clickable((
                    By.NAME,
                    input_name,
                ))
            )
            query_input = super().find_element_by_name(input_name)
            query_input.clear()
            query_input.send_keys(query)
            logger.info('Input query `%s`' % query)
        except NoSuchElementException:
            logger.error('Input not found `%s`' % input_name)
        except TimeoutException:
            logger.error('Timeout element not find `%s`' % input_name)

    def input_query_enter(self, input_name, query):
        try:
            query_input = super().find_element_by_name(input_name)
            query_input.clear()
            query_input.send_keys(query + Keys.RETURN)
            logger.info('Input query enter `%s`' % query)
            self.wait()
        except NoSuchElementException:
            logger.error('Input not found')

    def find_on_page_and_click_on(self, occurence):
        try:
            link_match = super().find_element_by_partial_link_text(occurence)
            link_match.click()
            logger.info('Occurence find ' + occurence)
            self.wait()
        except NoSuchElementException:
            logger.error('Occurence not found ' + occurence)

    def find_elements(self, by=By.CSS_SELECTOR, value=None):
        try:
            WebDriverWait(super(), self.timeout).until(
                EC.element_to_be_clickable((
                    by,
                    value,
                ))
            )
            list_link = super().find_elements(by, value)
            logger.info('Elements find `%s`' % value)
            return list_link
        except NoSuchElementException:
            logger.error('Elements not find `%s`' % value)
        except TimeoutException:
            logger.error('Timeout element not find `%s`' % value)
            return None

    def find_element(self, by=By.CSS_SELECTOR, value=None):
        try:
            WebDriverWait(super(), self.timeout).until(
                EC.element_to_be_clickable((
                    by,
                    value,
                ))
            )
            element = super().find_element(by, value)
            logger.info('Element find `%s`' % element)
            return element
        except NoSuchElementException:
            logger.error('Element not find `%s`' % value)
        except TimeoutException:
            logger.error('Timeout element not find `%s`' % value)
        return None

    def back(self):
        self.back()
        self.wait()
        logger.info('Navigation Back')

    def scroll_to_bottom(self):
        logger.info('Start scrolling')
        last_height = self.execute_script("return document.body.scrollHeight")
        while True:
            self.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);"
            )
            self.wait()
            new_height = self.execute_script(
                "return document.body.scrollHeight"
            )
            if new_height == last_height:
                break
            last_height = new_height
        logger.info('End scrolling')

    def wait_url(self, url):
        try:
            WebDriverWait(super(), self.timeout).until(EC.url_to_be(url))
            return url
        except TimeoutException:
            logger.error('Timeout wait url `%s`' % url)
            return None
