from accounts.models import Profile
from django import forms

class SearchForm(forms.ModelForm):
    class Meta:
        model=Profile
        fields=['user','department','program','year','last_test_taken']

    widgets = {
        'user': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Search Name','id':'id_user'}),
        'department': forms.Select(attrs={'class': 'form-control'}),
        'program': forms.Select(attrs={'class': 'form-control'}),
        'year': forms.Select(attrs={'class': 'form-control'}),
        'last_test_taken': forms.SelectDateWidget(attrs={'class': 'form-control'}),
    }