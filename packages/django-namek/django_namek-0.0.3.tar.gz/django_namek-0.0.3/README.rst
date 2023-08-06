************
Django Namek
************

.. image:: https://img.shields.io/pypi/v/django_namek
    :target: https://pypi.org/project/django_namek/

.. image:: https://img.shields.io/pypi/pyversions/django_namek
    :target: https://pypi.org/project/django_namek/

Django Namek is a Django app for forms chaining with some features :

- Manage Django forms in Django session
- Reuse generic `views <https://github.com/Aleksi44/django-namek/blob/master/django_namek/views.py>`_ : IndexView, ValidationView and ResultsView
- Perform an action with the results of the forms
- Tests written with Selenium


.. image:: https://d271q0ph7te9f8.cloudfront.net/www/documents/django_namek_preview.gif

Setup
#####


1 - Install with pip :

``pip install django_namek``


2 - Create your forms
::

    from django import forms
    from django_namek import abstract


    class LocationForm(abstract.Form):
        display_name = "Location"
        slug = "location"

        address_line = forms.CharField(
            label='Adresse',
            max_length=100
        )
        zip_code = forms.CharField(
            label='Postal Code',
            max_length=5
        )
        city = forms.CharField(
            label='City',
            max_length=100
        )


3 - Create your workflows
::

    from django_namek import abstract
    from . import forms


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


4 - Create an action :
::

    import hashlib
    from django_namek.actions import Action


    class Md5(Action):

        def run(self):
            address_line = self.session.get_field('address_line', '')
            zip_code = self.session.get_field('zip_code', '')
            city = self.session.get_field('city', '')
            activity = self.session.get_field('activity', ['empty'])

            md5 = hashlib.md5()

            md5.update(address_line.encode())
            md5.update(zip_code.encode())
            md5.update(city.encode())
            md5.update(activity[0].encode())

            self.res['md5'] = md5



5 - Change your Django settings.py. For more customization, take a look at `constants.py <https://github.com/Aleksi44/django-namek/blob/master/django_namek/constants.py>`_ :
::

    INSTALLED_APPS = [
        ...
        'django_namek',
    ]
    ...
    SESSION_ENGINE = "django_namek.session"
    DN_WORKFLOWS = [
        'tests.views.PersonWorkflow',
        'tests.views.CompanyWorkflow',
    ]
    DN_BASE_URL = "http://localhost:4243"
    DN_ACTION_CLASS = "tests.actions.Md5"


6 - Add Django Namek urls :
::

    from django.urls import include, path

    urlpatterns = [
        ...
        path('', include('django_namek.urls', namespace='django_namek'))
    ]


Optional : configure an email backend with django for validation view (example with `anymail[sendgrid] <https://anymail.readthedocs.io/en/stable/esps/sendgrid/>`_) :
::

    ANYMAIL = {
        "SENDGRID_API_KEY": xxxxxx,
    }
    EMAIL_BACKEND = "anymail.backends.sendgrid.EmailBackend"
    DEFAULT_FROM_EMAIL = "mail@example.com"
    SERVER_EMAIL = "mail@example.com"



Development env
###############

::

    git clone git@github.com:Aleksi44/django-namek.git
    pip install -r requirements.txt


Run Django Server
*****************

::

    python manage.py migrate
    python manage.py init
    python manage.py runserver 0.0.0.0:4243


Tests
#####

This test allows you to test all workflows with selenium :
::

    python manage.py test django_namek.tests
