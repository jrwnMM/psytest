from django.utils.translation import gettext_lazy as _
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.forms.widgets import Select, SelectDateWidget

from django.contrib.auth.forms import PasswordResetForm, PasswordChangeForm

from django.utils import timezone

import re

now = timezone.now()

class CreateUserForm(UserCreationForm):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields['password1'].label = 'Password'
        self.fields['password2'].label = 'Confirm Password'
        self.fields['email'].label = 'Email Address'
        self.fields['username'].label = 'Username'
        self.fields['first_name'].label = 'First Name'
        self.fields['last_name'].label = 'Last Name'
        self.fields['gender'].label = 'Gender'
        self.fields['date_of_birth'].label = 'Date of Birth'

    year_range = list(range(now.year-100, now.year+1))
    year_range.reverse()

    gender_choices = [
            ('', '---'),
            ('M', 'Male'),
            ('F', 'Female'),
        ]
    date_of_birth = forms.DateField(required = False, widget=SelectDateWidget(empty_label=("Year", "Month", "Day"), years=year_range, attrs={
        'class': 'form-select'
    }))
    gender = forms.CharField(widget=Select(choices=gender_choices, attrs={
        'class': 'form-select'
    }))
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Type your first name',
        'autofocus': ''
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Type your last name'
    }))
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Type your username'
    }))    
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Type your email address'
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Type your password'
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Re-enter password'
    }))
    is_superuser = forms.BooleanField(required=False,widget=forms.CheckboxInput(attrs={
        'placeholder': 'is_superuser'
    }))

    class Meta:
        model=User
        fields = ['first_name', 'last_name','gender','date_of_birth','username','email','password1','password2', 'is_superuser']

    def clean_first_name(self):
        if not self.cleaned_data.get('first_name').replace(" ", "").isalpha():
            raise ValidationError("it shouldn't contain numbers")
        
        return self.cleaned_data.get('first_name')

    def clean_last_name(self):
        if not self.cleaned_data.get('last_name').replace(" ", "").isalpha():
            raise ValidationError("it shouldn't contain numbers")
        
        return self.cleaned_data.get('last_name')

    def clean_date_of_birth(self):
        try:
            date = self.cleaned_data.get('date_of_birth')
        except:
            raise ValidationError('Enter a valid date')
            
        return self.cleaned_data.get('date_of_birth')

    def clean_username(self):
        pattern = '^[A-Za-z0-9]+(?:[ _-][A-Za-z0-9]+)*$'
        username = self.cleaned_data.get('username')
        result = re.match(pattern, username)
        if not result:
            raise ValidationError('Invalid Username')
        
        if len(username) < 6:
            raise ValidationError('Username must be minimum to 6 characters')

        return username

    def clean_password1(self):
        pattern = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$"
        password1 = self.cleaned_data.get('password1')
        result = re.match(pattern, password1)
        if not result:
            raise ValidationError('Invalid Password')
        
        return password1

    def clean_password2(self):
        if self.cleaned_data.get('password2') != self.cleaned_data.get('password1'):
            raise ValidationError("Confirmation password doesn't match")

        return self.cleaned_data.get('password2')

    def clean_email(self):
        pattern = '([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'
        email = self.cleaned_data.get('email')
        result = re.fullmatch(pattern, email)

        try:
            User.objects.get(email=email)
            raise ValidationError('Email address already exist')
        except ObjectDoesNotExist:
            pass

        if not result:
            raise ValidationError('Invalid email address')

        return self.cleaned_data.get('email')

class UpdateUserForm(forms.ModelForm):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields['email'].label = 'Email Address'
        self.fields['username'].label = 'Username'
        self.fields['first_name'].label = 'First Name'
        self.fields['last_name'].label = 'Last Name'

    first_name = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Type your first name',
    }))
    last_name = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Type your last name'
    }))
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Type your username'
    }))    
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Type your email address'
    }))
    is_superuser = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={
        'placeholder': 'is_superuser',
        'class': 'form-check-input',
    }))


    class Meta:
        model=User
        fields = ['first_name', 'last_name','username','email','is_superuser']

    def clean_first_name(self):
        if not self.cleaned_data.get('first_name').replace(" ", "").isalpha():
            raise ValidationError("it shouldn't contain numbers")
        
        return self.cleaned_data.get('first_name')

    def clean_last_name(self):
        if not self.cleaned_data.get('last_name').replace(" ", "").isalpha():
            raise ValidationError("it shouldn't contain numbers")
        
        return self.cleaned_data.get('last_name')

class CustomizedPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Type your email address'
    }))

class CustomizedPasswordResetConfirmForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Old password'
    }))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Type here'
    }))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Type here'
    }))

    def clean_new_password1(self):
        pattern = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$"
        new_password1 = self.cleaned_data.get('new_password1')
        result = re.match(pattern, new_password1)
        if not result:
            raise ValidationError('Invalid Password')
        
        return new_password1

    def clean_new_password2(self):
        if self.cleaned_data.get('new_password2') != self.cleaned_data.get('new_password1'):
            raise ValidationError("Confirmation password doesn't match")

        return self.cleaned_data.get('new_password2')
