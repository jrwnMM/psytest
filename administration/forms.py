from django import forms
from accounts.models import Profile

from personalityTest.models import Questionnaire
from riasec.models import RIASEC_Test

from personalityTest.models import Questionnaire
from riasec.models import RIASEC_Test
from administration.models import AdminScheduledConsultation


class SearchForm(forms.Form):
    name = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Search username',
    }))


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

