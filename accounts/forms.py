from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.forms.widgets import Select, SelectDateWidget
from django.contrib.auth.forms import PasswordResetForm
from django.utils import timezone

from dynamic_forms import DynamicField, DynamicFormMixin

import re

from phonenumber_field.formfields import PhoneNumberField

from accounts.models import Department, EducationLevel, Program, Year

now = timezone.now()
year_range = list(range(now.year - 100, now.year + 1))
year_range.reverse()

class CreateUserForm(DynamicFormMixin, UserCreationForm):
    def __init__(self, *args, **kwargs) -> None:
        super(CreateUserForm, self).__init__(*args, **kwargs)
        self.fields['password1'].label = 'Password'
        self.fields['password2'].label = 'Confirm Password'
        self.fields['email'].label = 'Email Address'
        self.fields['username'].label = 'Username'
        self.fields['first_name'].label = 'First Name'
        self.fields['last_name'].label = 'Last Name'
        self.fields['sex'].label = 'Sex'
        self.fields['date_of_birth'].label = 'Date of Birth'



    sex_choices = [
        ('', 'Please select one'),
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]

    date_of_birth = forms.DateField(required=True, widget=SelectDateWidget(empty_label=("Year", "Month", "Day"), years=year_range, attrs={
                                                                'class': 'form-select'
                                                            }))
    sex = forms.CharField(required=True,widget=Select(choices=sex_choices, attrs={
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
    middle_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Type your middle name'
    }))
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Type your username'
    }))
    contactNumber = PhoneNumberField(region="PH", widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Type your contact number'
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


    year_choices = lambda form: Year.objects.filter(educationlevel=form['educationlevel'].value() or None).order_by('name')
    department_choices = lambda form: Department.objects.filter(educationlevel=form['educationlevel'].value() or None).order_by('name')
    program_choices = lambda form: Program.objects.filter(department=form['department'].value() or None).order_by('name')
    

    educationlevel = forms.ModelChoiceField(
        queryset = EducationLevel.objects.all(),
        to_field_name= "id",
        widget= forms.Select(attrs={'class': 'form-select'}),
        )
    

    department = DynamicField(
        forms.ModelChoiceField,
        queryset = department_choices,
    )

    program = DynamicField(
        forms.ModelChoiceField,
        queryset=program_choices,
        required = False,
    )
    
    year = DynamicField(
        forms.ModelChoiceField,
        queryset = year_choices,
    )

    class Meta:
        model = User
        fields = ['first_name', 'middle_name', 'last_name', 'sex', 'date_of_birth', 'contactNumber', 'username',
                  'email', 'password1', 'password2', 'educationlevel', 'department', 'program', 'year']

    def clean_first_name(self):
        if not self.cleaned_data.get('first_name').replace(" ", "").isalpha():
            raise ValidationError("it shouldn't contain numbers")

        return self.cleaned_data.get('first_name').title()

    def clean_middle_name(self):
        if not self.cleaned_data.get('middle_name').replace(" ", "").isalpha():
            raise ValidationError("it shouldn't contain numbers")

        return self.cleaned_data.get('middle_name').title()

    def clean_last_name(self):
        if not self.cleaned_data.get('last_name').replace(" ", "").isalpha():
            raise ValidationError("it shouldn't contain numbers")

        return self.cleaned_data.get('last_name').title()

    def clean_date_of_birth(self):
        try:
            date = self.cleaned_data.get('date_of_birth')
        except:
            raise ValidationError('Enter a valid date')

        return date

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
        password1 = self.cleaned_data.get('password1')
        pattern = "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9]).{8,}$"
        pat = re.compile(pattern)            
        mat = re.search(pat, password1)
        if mat:
            return password1
        else:
            raise ValidationError("Invalid Password")

        

    def clean_password2(self):
        if self.cleaned_data.get('password1') is None:
            pass
        elif self.cleaned_data.get('password2') != self.cleaned_data.get('password1'):
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


    

class CustomizedPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Type your email address'
    }))


class CustomizedPasswordResetConfirmForm(SetPasswordForm):
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
