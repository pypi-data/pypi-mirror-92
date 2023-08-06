import logging

logger = logging.getLogger('django_namek')


class Action(object):
    session = None
    res = None
    workflows = None

    def __init__(self, session):
        self.session = session

    def log_results(self):
        for key, value in self.res.items():
            logger.debug('%s=`%s`' % (
                key,
                value
            ))

    def with_path(self, path):
        return path in self.workflows

    def run(self):
        return

    def get_results(self):
        """Get the values for all the forms and run all calculations"""
        self.res = {}  # Reset results dict and session fields
        self.session.refresh_forms()
        self.workflows = self.session['workflows']
        self.run()
        return self.res
