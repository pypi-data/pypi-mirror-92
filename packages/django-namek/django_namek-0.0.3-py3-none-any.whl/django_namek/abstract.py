import json
import logging
from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.utils.text import slugify
from django.contrib.sessions.base_session import AbstractBaseSession
from django.db import models
from django.shortcuts import reverse
from django import forms

from .session import SessionStore
from . import constants

logger = logging.getLogger('django_namek')


class BaseView(TemplateView):

    def reverse_app(self, path, params):
        return reverse(
            "django_namek:%s" % path,
            kwargs=params
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['version'] = constants.DN_VERSION
        context['debug'] = constants.DN_DEBUG
        context['constants'] = constants

        # Convert module 'constants' to json for javascript
        ret = {}
        for k, v in constants.__dict__.items():
            if 'DN_' in k:
                ret[k] = v
        context['constants_json'] = json.dumps(ret)

        return context


class WorkflowView(BaseView):
    slug = None
    forms = []
    session = None
    step = 0
    django_form = None
    next = None

    @property
    def start_url(self):
        return self.reverse_app(
            self.path,
            {'slug': '0'}
        )

    @property
    def path(self):
        return slugify(self.slug)

    def render_final_view(self):
        if constants.DN_WORKFLOW_REDIRECT_RESULTS:
            return self.render_results_view()
        return self.render_validation_view()

    def render_validation_view(self):
        return redirect(self.reverse_app(
            'validation',
            {}
        ))

    def render_results_view(self):
        return redirect(self.reverse_app(
            'results',
            {'session_key': self.session.session_key}
        ))

    def render_next(self):
        return redirect(self.reverse_app(
            self.path,
            {'slug': self.get_form(self.step + 1).slug}
        ))

    def get_form(self, step=-1):
        if step == -1:
            step = self.step
        return self.forms[step]

    def get_step(self, slug):
        counter = 0
        for form in self.forms:
            if form.slug == slug:
                return counter
            counter += 1
        # raise error here
        return 0

    def get_django_form(self):
        return self.get_form()

    def get_django_form_session(self):
        form_data = self.session.get_form_data(
            self.path,
            self.get_form().slug
        )
        if not form_data:
            # Return form without data
            return self.get_django_form()
        else:
            # Return form with data
            return self.get_django_form()(form_data)

    def get_context_data(self, request, slug, *args, **kwargs):
        context = super().get_context_data(**kwargs)

        # Init some variables

        self.next = request.GET.get('next', None)
        self.session = request.session
        self.step = self.get_step(slug)

        logger.debug('WITH workflow_path=%s' % self.path)
        logger.debug('WITH form_slug=%s' % self.get_form().slug)

        self.django_form = self.get_django_form_session()
        self.template_name = self.get_form()().get_template()

        context['self'] = self
        context['workflow_step'] = self.step
        context['workflow'] = self.session.load_workflow()
        context['form'] = self.django_form

        # Check next and prev form
        if self.step < len(self.forms) - 1:
            context['next'] = True
            context['next_url'] = self.reverse_app(
                self.path,
                {'slug': self.get_form(self.step + 1).slug}
            )
        if self.step > 0:
            context['prev'] = True
            context['prev_url'] = self.reverse_app(
                self.path,
                {'slug': self.get_form(self.step - 1).slug}
            )
        return context

    def get(self, request, slug=None, *args, **kwargs):
        context = self.get_context_data(request, slug, **kwargs)
        logger.debug('WITH step=%s' % self.step)
        if self.step == 0:
            self.session.clear_forms()
        return self.render_to_response(context)

    def post(self, request, slug=None, *args, **kwargs):
        context = self.get_context_data(request, slug, **kwargs)
        form_posted = self.get_django_form()(request.POST)

        if form_posted.is_valid():
            self.session.set_form_data(
                self.path,
                self.get_form().slug,
                form_posted.clean()
            )

            # Next view is specified in url
            if self.next:
                return redirect(self.next)

            # Success -> Final View
            if 'next' not in context:
                return self.render_final_view()

            # Success -> Next View
            return self.render_next()
        else:
            # Form is not valid, retry
            context['form'] = form_posted
            return self.render_to_response(context)


class AbstractWorkflow(AbstractBaseSession):
    email = models.EmailField(null=True, default=None)

    @property
    def url_results(self):
        return reverse(
            "django_namek:results",
            kwargs={'session_key': self.session_key}
        )

    @property
    def url_full_results(self):
        return constants.DN_BASE_URL + self.url_results

    @classmethod
    def get_session_store_class(cls):
        return SessionStore

    class Meta:
        verbose_name = 'Workflow'
        verbose_name_plural = 'Workflows'
        abstract = True


class Form(forms.Form):
    display_name = 'Not defined'
    template_name = None
    slug = None

    def get_template(self):
        if not self.template_name:
            return 'django_namek/forms/form.html'
        return self.template_name
