from django import forms


# Others forms

class ValidationForm(forms.Form):
    mail = forms.EmailField(label='Email')
