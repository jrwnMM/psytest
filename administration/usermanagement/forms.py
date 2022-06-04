from django import forms
from django.contrib.auth import get_user_model
User = get_user_model()

class AdminSearchForm(forms.ModelForm):
    # name = forms.CharField(required=False, widget=forms.TextInput(attrs={
    #     'class': 'form-control',
    #     'placeholder': 'Search Name',
    # }))
    #
    class Meta:
        model=User
        fields = ['username','first_name','last_name','is_superuser','date_joined','email']

    widgets = {
        'username': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Search Name','id':'id_user'}),
        'first_name': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Search Firstname'}),
        'last_name': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Search Lastname'}),
        'email': forms.EmailInput(attrs={'class': 'form-control','placeholder': 'Search Email'}),
        'date_joined': forms.SelectDateWidget(attrs={'class': 'form-control'}),
        'is_superuser': forms.CheckboxInput(attrs={'class': 'form-control'}),
    }