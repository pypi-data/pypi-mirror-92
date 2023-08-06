import logging
from django_namek import abstract

from . import forms

logger = logging.getLogger('app')


class PersonWorkflow(abstract.WorkflowView):
    display_name = 'Person'
    slug = 'person'
    forms = [
        forms.LocationForm,
        forms.ActivityForm,
    ]


class CompanyWorkflow(abstract.WorkflowView):
    display_name = 'Company'
    slug = 'company'
    forms = [
        forms.LocationForm,
        forms.ActivityForm,
    ]
