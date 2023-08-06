from django_namek.tests.test_case import SeleniumTestCase
from django.shortcuts import reverse

from django_namek import constants
from django_namek import utils


class WorkflowsTest(SeleniumTestCase):

    def test_workflows(self):
        for workflow_str in constants.DN_WORKFLOWS:
            workflow = utils.import_from_string(workflow_str)()
            workflow_url = reverse(
                "django_namek:%s" % workflow.path,
                kwargs={'slug': 0}
            )
            self.selenium.get("%s%s" % (constants.DN_BASE_URL, workflow_url))
            while '/results/' not in self.selenium.current_url:
                self.workflow.fill_form(workflow.forms[0])
                self.workflow.submit()
