from django import forms
from accounts.models import Department, Program
from django.core.exceptions import ValidationError

class AddDepartmentForm(forms.ModelForm):   
    class Meta:
        model=Department
        fields = ('code', 'name')
        widgets = {
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class AddProgramForm(forms.ModelForm):
    class Meta:
        model = Program
        fields = ('department', 'name', 'code')
        widgets = {
            'department': forms.Select(attrs={'class': 'form-select'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
        }
    