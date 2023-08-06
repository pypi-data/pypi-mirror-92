from django.urls import path
from django.conf import settings
from django.utils.text import slugify
from . import utils
from . import constants

app_name = 'django_namek'

urlpatterns = []

index_view = utils.import_from_string(constants.DN_INDEX_VIEW)
urlpatterns.append(
    path(
        slugify(index_view.slug),
        index_view.as_view(),
        name='index'
    )
)

validation_view = utils.import_from_string(constants.DN_VALIDATION_VIEW)
urlpatterns.append(
    path(
        slugify(validation_view.slug),
        validation_view.as_view(),
        name='validation'
    )
)

result_view = utils.import_from_string(constants.DN_RESULT_VIEW)
urlpatterns.append(
    path(
        '%s/<str:session_key>/' % result_view.slug,
        result_view.as_view(),
        name='results'
    )
)

for workflow in settings.DN_WORKFLOWS:
    workflow_view = utils.import_from_string(workflow)
    urlpatterns.append(
        path(
            '%s/<str:slug>/' % slugify(workflow_view.slug),
            workflow_view.as_view(),
            name=slugify(workflow_view.slug)
        )
    )
