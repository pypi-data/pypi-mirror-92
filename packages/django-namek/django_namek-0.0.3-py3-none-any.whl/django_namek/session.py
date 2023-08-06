import logging
from django.contrib.sessions.backends.db import SessionStore as DBStore
from django.shortcuts import reverse

from . import utils
from . import constants

logger = logging.getLogger('django_namek')


class SessionStore(DBStore):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.all_forms = utils.get_all_forms()

    @classmethod
    def get_model_class(cls):
        return utils.import_from_string(constants.DN_BASE_SESSION)

    def set_form_data(self, workflow_path, form_slug, form_data):
        if 'forms' not in self:
            self['forms'] = {}
        if workflow_path not in self['forms']:
            self['forms'][workflow_path] = {}
        self['forms'][workflow_path][form_slug] = form_data
        self.save()
        return

    def get_form_data(self, workflow_path, form_slug):
        if 'forms' not in self:
            self['forms'] = {}
        if workflow_path not in self['forms']:
            self['forms'][workflow_path] = {}
        if form_slug not in self['forms'][workflow_path]:
            return None
        return self['forms'][workflow_path][form_slug]

    def clear_forms(self):
        self['forms'] = {}

    def load_workflow(self):
        return self._get_session_from_db()

    def load_forms(self):
        ret = []
        workflow = self._get_session_from_db()
        if 'forms' in self:
            for workspace_path, workspace_forms \
                    in self['forms'].items():
                for form_slug, form_content \
                        in self['forms'][workspace_path].items():
                    ret.append({
                        'form': self.all_forms[form_slug](form_content),
                        'edit_url_validation': reverse(
                            "django_namek:%s" % workspace_path,
                            kwargs={'slug': form_slug}
                        ) + '?next=%s' % reverse('django_namek:validation'),
                        'edit_url_results': reverse(
                            "django_namek:%s" % workspace_path,
                            kwargs={'slug': form_slug}
                        ) + '?next=%s' % reverse(
                            'django_namek:results',
                            kwargs={'session_key': workflow.session_key}
                        ),
                    })
        return ret

    def refresh_forms(self):
        self['fields'] = {}
        self['workflows'] = []
        if 'forms' in self:
            for workspace_path, workspace_forms \
                    in self['forms'].items():
                self['workflows'].append(workspace_path)
                for form_slug, form_content \
                        in self['forms'][workspace_path].items():
                    if form_content:
                        for key, value in form_content.items():
                            self['fields'][key] = value
        return 0

    def get_field(self, key, default=None):
        if 'fields' not in self:
            return default
        if key not in self['fields']:
            return default
        return self['fields'][key]
