from django.utils.translation import gettext_lazy as _
from django import forms
from django.core.exceptions import  ValidationError
from django.utils import timezone

from dynamic_forms import DynamicField, DynamicFormMixin

from phonenumber_field.formfields import PhoneNumberField

from accounts.models import Department, EducationLevel, Profile, Program, Year

now = timezone.now()
year_range = list(range(now.year - 100, now.year + 1))
year_range.reverse()

class UpdateProfileForm(DynamicFormMixin, forms.ModelForm):

    department_choices = lambda form: Department.objects.filter(educationlevel=form['educationlevel'].value() or None).order_by('name')
    year_choices = lambda form: Year.objects.filter(educationlevel=form['educationlevel'].value() or None).order_by('name')
    program_choices = lambda form: Program.objects.filter(department=form['department'].value() or None).order_by('name')

    def __init__(self, *args, **kwargs) -> None:
        super(UpdateProfileForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].label = 'First Name'
        self.fields['last_name'].label = 'Last Name'
        self.fields['date_of_birth'].label = 'Date of Birth'
        self.fields['sex'].label = 'Sex'
        self.fields['contactNumber'].label = 'Contact Number'
        self.fields['middle_name'].label = 'Middle Name'
        self.fields['educationlevel'].label = 'Education Level'
        self.fields['department'].label = 'Department'
        self.fields['program'].label = 'Program'
        self.fields['year'].label = 'Year'

    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Type your first name',
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Type your last name'
    }))

    contactNumber = PhoneNumberField(region="PH" ,widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Type your contact number'
    }))


    educationlevel = forms.ModelChoiceField(
        queryset=EducationLevel.objects.all(), 
        to_field_name='id', 
        widget=forms.Select(attrs={'class': 'form-select'}))

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
        model = Profile
        fields = ['first_name', 'last_name', 'date_of_birth','sex','contactNumber','middle_name','educationlevel','department','program','year']
        widgets = {
            'middle_name': forms.TextInput(attrs={'class': 'form-control'}),
            'date_of_birth': forms.SelectDateWidget(empty_label=("Year", "Month", "Day"), years=year_range, attrs={'class': 'form-select', 'required': True,}),
            'sex': forms.Select(attrs={'class': 'form-select', 'required': True,}),
        }

    def clean_first_name(self):
        if not self.cleaned_data.get('first_name').replace(" ", "").isalpha():
            raise ValidationError("it shouldn't contain numbers")

        return self.cleaned_data.get('first_name').title()

    def clean_last_name(self):
        if not self.cleaned_data.get('last_name').replace(" ", "").isalpha():
            raise ValidationError("it shouldn't contain numbers")

        return self.cleaned_data.get('last_name').title()