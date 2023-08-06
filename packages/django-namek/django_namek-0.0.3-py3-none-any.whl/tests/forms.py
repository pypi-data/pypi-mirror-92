from django import forms
from django_namek import abstract

ACTIVITY_CHOICES = [
    ("dev", "Developer"),
    ("designer", "Designer"),
]


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


class ActivityForm(abstract.Form):
    display_name = "Activity"
    slug = "activity"

    activity = forms.MultipleChoiceField(
        label='Activity',
        choices=ACTIVITY_CHOICES
    )
