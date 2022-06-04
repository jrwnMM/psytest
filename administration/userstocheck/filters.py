import django_filters
from django import forms
from django_filters import (
    DateFilter,
    CharFilter,
    ModelChoiceFilter,
)
from accounts.models import Profile, EducationLevel, Program, Year
from django.db.models import Q


class ProfileFilter(django_filters.FilterSet):
    start_date = DateFilter(field_name='last_test_taken', lookup_expr='gte', label='Last Test Taken (Start)',
                            widget=forms.DateInput(attrs={'class': 'form-control'}))
    end_date = DateFilter(field_name='last_test_taken', lookup_expr='lte', label='Last Test Taken (End)',
                          widget=forms.DateInput(attrs={'class': 'form-control'}))

    date_completed_order = DateFilter(
        field_name='last_test_taken',
        lookup_expr='exact',
        label='Last Test Taken',
        widget=forms.DateInput(attrs={'class': 'form-control'})
    )

    user = CharFilter(method='user_filter', label='User', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Search Name',
    }))

    department__name = ModelChoiceFilter(queryset=EducationLevel.objects.all(),
                                         widget=forms.Select(attrs={'class': 'form-control'}), )
    program__name = ModelChoiceFilter(queryset=Program.objects.all(),
                                      widget=forms.Select(attrs={'class': 'form-control'}), )
    year__name = ModelChoiceFilter(queryset=Year.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}), )

    class Meta:
        model = Profile
        fields = ['user', 'department', 'program', 'year', 'last_test_taken']
        exclude = ['is_assigned', 'is_result']

    def user_filter(self, queryset, name, value):
        for term in value.split():
            queryset = queryset.filter(Q(user__first_name__icontains=term) | Q(user__last_name__icontains=term))
            return queryset