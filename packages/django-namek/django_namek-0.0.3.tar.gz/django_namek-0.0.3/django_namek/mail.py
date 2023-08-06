import logging
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import get_template

from . import constants

logger = logging.getLogger('django_namek')

VALIDATION_MAIL = {
    'subject': 'Valider vos informations',
    'from': settings.DEFAULT_FROM_EMAIL,
    'id': 'validation'
}


def load_html(template, session):
    html = get_template('django_namek/mails/%s.html' % template['id'])
    template['html'] = html.render({
        'workflow': session.load_workflow(),
        'session_forms': session.load_forms(),
        'constants': constants
    })
    return template


def send_mail(mail, template, session):
    template = load_html(template, session)
    msg = EmailMultiAlternatives(
        template['subject'],
        '',
        template['from'],
        [mail]
    )
    msg.attach_alternative(template['html'], "text/html")
    msg.send()
    logger.debug('SEND mail %s' % template['html'])
