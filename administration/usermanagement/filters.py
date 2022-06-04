from django.contrib.auth import get_user_model
from django import forms
from django.db.models import Q

import django_filters
from django_filters import (DateFilter,CharFilter)

User = get_user_model()

class UserFilter(django_filters.FilterSet):
    username = CharFilter(method='user_filter', label='User', widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))
    date_joined=DateFilter(widget=forms.DateInput(attrs={'class': 'form-control'}))
    start_date = DateFilter(field_name='date_joined', lookup_expr='gte', label='Date Joined (Start)',
                            widget=forms.DateInput(attrs={'class': 'form-control'}))
    end_date = DateFilter(field_name='date_joined', lookup_expr='lte', label='Date Joined (End)',
                          widget=forms.DateInput(attrs={'class': 'form-control'}))
    # is_superuser = BooleanFilter(field_name='is_superuser', lookup_expr='exact', label='Is_superuser',
    #                              widget=forms.CheckboxInput(attrs={'class': 'form-check-input','type':'checkbox',}))

    class Meta:
        model = User
        fields = ['username', 'last_name', 'first_name', 'is_superuser', 'date_joined', 'email']

    def user_filter(self, queryset, name, value):
        for term in value.split():
            queryset = queryset.filter(
                Q(first_name__icontains=term) | Q(last_name__icontains=term) | Q(username__icontains=term) | Q(
                    email__icontains=term))
            return queryset