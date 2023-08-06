import logging
from django.http import Http404
from django.shortcuts import redirect, reverse

from . import abstract
from . import session
from . import utils
from . import mail
from . import forms
from . import exceptions
from . import constants

logger = logging.getLogger('django_namek')


class IndexView(abstract.BaseView):
    template_name = "django_namek/index.html"
    slug = ''

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['workflows'] = []
        for workflow_view_string in constants.DN_WORKFLOWS:
            workflow_view = utils.import_from_string(workflow_view_string)()
            context['workflows'].append(workflow_view)
        return context


class ValidationView(abstract.BaseView):
    template_name = 'django_namek/validation.html'
    slug = 'validation'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        # Redirect to ResultsView if mail is validated

        mail_validated = request.session.get('mail_validated', False)
        if mail_validated:
            workflow = request.session.load_workflow()
            return redirect(reverse(
                'django_namek:results',
                kwargs={'session_key': workflow.session_key}
            ))

        context['session_forms'] = request.session.load_forms()
        context['form_validation'] = forms.ValidationForm()
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        mail_form = request.POST.get('mail', 'None')
        if mail_form:
            workflow = request.session.load_workflow()
            workflow.email = mail_form
            workflow.save()
            mail.send_mail(
                mail_form,
                mail.VALIDATION_MAIL,
                request.session
            )
        request.session['email_session'] = mail_form
        context['is_validated'] = True
        return self.render_to_response(context)


class ResultsView(abstract.BaseView):
    template_name = 'django_namek/results.html'
    slug = 'results'

    def get(self, request, session_key=None, *args, **kwargs):
        if not session_key:
            raise Http404
        request.session = session.SessionStore(session_key=session_key)
        request.session['mail_validated'] = True
        context = self.get_context_data(**kwargs)
        context['session_forms'] = request.session.load_forms()
        try:
            action_class = utils.import_from_string(constants.DN_ACTION_CLASS)
            action = action_class(request.session)
            context['action'] = action.get_results()
        except exceptions.ActionError as err:
            context['error'] = err
        return self.render_to_response(context)
