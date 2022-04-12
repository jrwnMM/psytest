import django_filters
import operator
from django import forms
from django_filters import (
    DateFilter,
    CharFilter,
    OrderingFilter,
    AllValuesFilter,
    ChoiceFilter,
    ModelChoiceFilter,
    BooleanFilter,
)
from django_filters.widgets import LinkWidget
from django.forms.widgets import Select, SelectDateWidget
from django.contrib.auth.models import User
from accounts.models import Profile, Department, Program, Year
from django.db.models import Q


class ProfileFilter(django_filters.FilterSet):
    start_date = DateFilter(field_name='test_completed', lookup_expr='gte', label='Date Completed (Start)',
                            widget=forms.DateInput(attrs={'class': 'form-control'}))
    end_date = DateFilter(field_name='test_completed', lookup_expr='lte', label='Date Completed (End)',
                          widget=forms.DateInput(attrs={'class': 'form-control'}))

    date_completed_order = DateFilter(
        field_name='test_completed',
        lookup_expr='exact',
        label='Date Completed',
        widget=forms.DateInput(attrs={'class': 'form-control'})
    )

    user = CharFilter(method='user_filter', label='User', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Search Name',
    }))

    department__name = ModelChoiceFilter(queryset=Department.objects.all(),
                                         widget=forms.Select(attrs={'class': 'form-control'}), )
    program__name = ModelChoiceFilter(queryset=Program.objects.all(),
                                      widget=forms.Select(attrs={'class': 'form-control'}), )
    year__name = ModelChoiceFilter(queryset=Year.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}), )

    # user__full_name=CharFilter(field_name='user__first_name',lookup_expr='icontains')
    # user__last_name=CharFilter(field_name='user__last_name',lookup_expr='icontains')

    class Meta:
        model = Profile
        fields = ['user', 'department', 'program', 'year', 'test_completed']
        exclude = ['is_assigned', 'is_result']

    def user_filter(self, queryset, name, value):
        for term in value.split():
            queryset = queryset.filter(Q(user__first_name__icontains=term) | Q(user__last_name__icontains=term))
            return queryset


class UserFilter(django_filters.FilterSet):
    username = CharFilter(method='user_filter', label='User', widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))
    date_joined=DateFilter(widget=forms.DateInput(attrs={'class': 'form-control'}))
    start_date = DateFilter(field_name='date_joined', lookup_expr='gte', label='Date Joined (Start)',
                            widget=forms.DateInput(attrs={'class': 'form-control'}))
    end_date = DateFilter(field_name='date_joined', lookup_expr='lte', label='Date Joined (End)',
                          widget=forms.DateInput(attrs={'class': 'form-control'}))
    is_superuser = BooleanFilter(field_name='is_superuser', lookup_expr='exact', label='Is_superuser',
                                 widget=forms.CheckboxInput(attrs={'class': 'form-check-input','type':'checkbox',}))

    class Meta:
        model = User
        fields = ['username', 'last_name', 'first_name', 'is_superuser', 'date_joined', 'email']

    def user_filter(self, queryset, name, value):
        for term in value.split():
            queryset = queryset.filter(
                Q(first_name__icontains=term) | Q(last_name__icontains=term) | Q(username__icontains=term) | Q(
                    email__icontains=term))
            return queryset
