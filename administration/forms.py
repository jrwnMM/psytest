from django import forms
from accounts.models import Profile
from administration.models import AdminScheduledConsultation

class ScheduleDateForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(ScheduleDateForm, self).__init__(*args, **kwargs)
        self.fields['managed_by'].label = 'Assigned to: '

    scheduled_date = forms.DateTimeField(required=True, widget=forms.DateTimeInput(attrs={
        'type': 'datetime-local',
        'class': 'form-control'
    }))

    managed_by = forms.ModelChoiceField(required=True, queryset=Profile.objects.filter(user__is_superuser=True), widget=forms.Select(attrs={
        'class': 'form-select'
    }))
    client = forms.ModelChoiceField(required=True, queryset=Profile.objects.all(), widget=forms.HiddenInput(attrs={
        'class': 'form-select'
    }))


