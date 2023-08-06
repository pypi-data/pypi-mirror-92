from django import test
import logging
from selenium.webdriver.common.by import By
from .client import Client
from .events.workflow import WorkflowEvent
from .faker import Faker
from webdriver_manager.chrome import ChromeDriverManager


class SeleniumTestCase(test.TestCase):
    selenium = None
    by = By

    def setUp(self):
        super().setUp()
        self.logging_tests = logging.getLogger('tests')
        self.selenium = Client(ChromeDriverManager().install())
        self.faker = Faker()
        self.workflow = WorkflowEvent(self)
