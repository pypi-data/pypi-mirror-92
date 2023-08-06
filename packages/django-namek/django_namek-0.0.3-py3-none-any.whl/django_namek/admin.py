import csv
import datetime

from django.contrib import admin
from django.http import HttpResponse

from .models import Workflow


class Export:
    keys = ['email', 'results']
    queryset = None

    def __init__(self, queryset):
        self.queryset = queryset
        self.response = HttpResponse(content_type='text/csv')
        self.response['Content-Disposition'] = \
            "attachment; filename=export-%s.csv" % \
            datetime.datetime.now().strftime('%d/%m/%Y')
        self.writer = csv.writer(self.response)

        # Heading

        for obj in self.queryset:
            decoded = obj.get_decoded()
            self.load_key(decoded)
        self.writer.writerow(self.keys)

        # Body

        for obj in queryset:
            data_row = [''] * len(self.keys)
            decoded = obj.get_decoded()
            data_row[0] = obj.email
            data_row[1] = obj.url_full_results
            data_row = self.load_values(decoded, data_row)
            self.writer.writerow(data_row)

    def load_key(self, data):
        for key, value in data.items():
            if isinstance(value, dict):
                self.load_key(value)
            else:
                if key not in self.keys and not key.startswith('_'):
                    self.keys.append(key)

    def load_values(self, data, data_row):
        for key, value in data.items():
            if isinstance(value, dict):
                self.load_values(value, data_row)
            else:
                try:
                    index = self.keys.index(key)
                    data_row[index] = value
                except ValueError:
                    pass
        return data_row


def export_csv(modeladmin, request, queryset):
    exp = Export(queryset)
    return exp.response


class WorkflowAdmin(admin.ModelAdmin):
    @staticmethod
    def _forms_data(obj):
        return obj.get_decoded()

    actions = [export_csv]
    list_display = [
        'session_key',
        'email',
        'url_full_results',
        '_forms_data',
        'expire_date'
    ]


admin.site.register(Workflow, WorkflowAdmin)
