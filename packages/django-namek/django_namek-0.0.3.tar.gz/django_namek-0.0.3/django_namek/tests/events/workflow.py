import logging
from django.forms import fields

from django_namek import utils
from ._event import Event

logger = logging.getLogger('tests')
ii = isinstance


class WorkflowEvent(Event):

    def submit(self):
        submit = self.tc.selenium.find_element(
            self.tc.by.XPATH,
            "//input[@type='submit']",
        )
        submit.click()
        logger.info('Submit form')

    def init_test_values(self):
        return {
            'address_line': 'Street',
            'zip_code': '66000',
            'city': 'test',
            'operating_result': '10000',
            'amortization': '1000',
            'charges': '1000',
            'remuneration': '1000',
        }

    def refresh_form(self, form):
        form_slug = self.tc.selenium.current_url.split('/')[-2]
        all_forms = utils.get_all_forms()
        if form_slug in all_forms:
            return all_forms[form_slug]
        return form

    def fill_form(self, form):
        try:

            form = self.refresh_form(form)

            test_values = self.init_test_values()
            form_fields = form.base_fields

            for field_name in form_fields:
                value = '1'
                if field_name in test_values:
                    value = test_values[field_name]

                if ii(form_fields[field_name], fields.MultipleChoiceField):
                    first_option = self.tc.selenium.find_element(
                        self.tc.by.XPATH,
                        "//select[@name='%s']/option" % field_name,
                    )
                    first_option.click()
                elif ii(form_fields[field_name], fields.ChoiceField):
                    inputs = self.tc.selenium.find_elements(
                        self.tc.by.NAME,
                        field_name,
                    )
                    inputs[0].click()
                elif ii(form_fields[field_name], fields.BooleanField):
                    input = self.tc.selenium.find_element(
                        self.tc.by.NAME,
                        field_name,
                    )
                    input.click()
                else:
                    self.tc.selenium.input_query(field_name, value)
        except Exception as err:
            logger.error(str(err))
            import pdb
            pdb.set_trace()
