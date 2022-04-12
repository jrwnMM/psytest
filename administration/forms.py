from django import forms
from accounts.models import Profile
from django.contrib.auth.models import User
from personalityTest.models import Questionnaire
from riasec.models import RIASEC_Test
from django.forms.widgets import Select, SelectDateWidget
from personalityTest.models import Questionnaire
from riasec.models import RIASEC_Test
from administration.models import AdminScheduledConsultation


class SearchForm(forms.ModelForm):
    class Meta:
        model=Profile
        fields=['user','department','program','year','test_completed']

    widgets = {
        'user': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Search Name','id':'id_user'}),
        'department': forms.Select(attrs={'class': 'form-control'}),
        'program': forms.Select(attrs={'class': 'form-control'}),
        'year': forms.Select(attrs={'class': 'form-control'}),
        'test_completed': forms.SelectDateWidget(attrs={'class': 'form-control'}),
    }

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
class AddRQuestionsForm(forms.ModelForm):
    class Meta:
        model = RIASEC_Test
        fields = ('question', 'category')

        category_choices = [
            ('R', 'Realistic'),
            ('I', 'Investigative'),
            ('A', 'Artistic'),
            ('S', 'Social'),
            ('E', 'Enterprising'),
            ('C', 'Conventional'),
        ]
        widgets = {
            'question': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}, choices=category_choices),
        }


class AddPQuestionsForm(forms.ModelForm):
    class Meta:
        model = Questionnaire
        fields = ('question', 'category', 'key')

        category_choices = [
            ('EXT', 'Extroversion'),
            ('EST', 'Neurotic'),
            ('AGR', 'Agreeable'),
            ('CSN', 'Conscientious'),
            ('OPN', 'Openness'),
        ]

        key_choices = [
            ('1', 'Positive'),
            ('0', 'Negative')
        ]

        widgets = {
            'question': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}, choices=category_choices),
            'key': forms.Select(attrs={'class': 'form-select'}, choices=key_choices),
        }


class ScheduleDateForm(forms.ModelForm):

    scheduled_date = forms.DateTimeField(required=True, widget=forms.DateTimeInput(attrs={
        'type': 'datetime-local',
        'class': 'form-control'
    }))

    managed_by = forms.ModelChoiceField(required=True, queryset=Profile.objects.filter(user__is_superuser=True), widget=forms.Select(attrs={
        'class': 'form-select'
    }))
    user = forms.ModelChoiceField(required=True, queryset=Profile.objects.all(), widget=forms.HiddenInput(attrs={
        'class': 'form-select'
    }))
    is_done = forms.BooleanField(required=False, widget=forms.HiddenInput())


    class Meta:
        model = AdminScheduledConsultation
        fields = ['scheduled_date', 'managed_by', 'user', 'is_done']


