import hashlib
import logging
from django_namek.actions import Action

logger = logging.getLogger('tests')


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
