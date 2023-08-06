import os
import json
import pkg_resources
from django.conf import settings

try:
    #  Production part
    DN_VERSION = pkg_resources.get_distribution("django_namek").version
except pkg_resources.DistributionNotFound:
    #  Develop part
    with open(os.path.join(settings.BASE_DIR, 'package.json')) as package:
        data = json.load(package)
        DN_VERSION = data['version']

DN_DEBUG = getattr(settings, "DEBUG", True)
DN_BASE_URL = getattr(settings, "DN_BASE_URL", "http://localhost:4243")

DN_TEST_BROWSER_OPEN = getattr(settings, "DN_TEST_BROWSER_OPEN", True)
DN_TEST_FAKER_LOCATION = getattr(settings, "DN_TEST_FAKER_LOCATION", "fr_FR")

DN_WORKFLOW_REDIRECT_RESULTS = getattr(
    settings,
    "DN_WORKFLOW_REDIRECT_RESULTS",
    DN_DEBUG
)
DN_WORKFLOWS = getattr(settings, "DN_WORKFLOWS", [])

DN_BASE_SESSION = getattr(
    settings,
    "DN_BASE_SESSION",
    "django_namek.models.Workflow"
)

DN_RESULT_VIEW = getattr(
    settings,
    "DN_RESULT_VIEW",
    "django_namek.views.ResultsView"
)
DN_VALIDATION_VIEW = getattr(
    settings,
    "DN_VALIDATION_VIEW",
    "django_namek.views.ValidationView"
)
DN_INDEX_VIEW = getattr(
    settings,
    "DN_INDEX_VIEW",
    "django_namek.views.IndexView"
)
DN_ACTION_CLASS = getattr(
    settings,
    "DN_ACTION_CLASS",
    "django_namek.actions.Action"
)

DN_BRAND_NAME = getattr(settings, "DN_BRAND_NAME", "Namek")
DN_BRAND_WEBSITE = getattr(
    settings,
    "DN_BRAND_WEBSITE",
    "https://fr.wikipedia.org/wiki/Namek"
)
DN_BRAND_COLOR_PRIMARY = getattr(settings, "DN_BRAND_COLOR_PRIMARY", '#ffcf00')
DN_BRAND_COLOR_SECONDARY = getattr(
    settings,
    "DN_BRAND_COLOR_SECONDARY",
    '#070707'
)
