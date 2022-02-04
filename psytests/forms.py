

from django import forms
from django import forms
from django.forms import widgets

class ContactForm(forms.Form):
    subject = forms.CharField(required=True ,max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    message = forms.CharField(required=True, max_length=360, widget=forms.Textarea(attrs={
        'class': 'form-control'
    }))