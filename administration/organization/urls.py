from django.urls import path
from .views import (DepartmentListView, add_education_level, edu_level_options, delete_education_level)

urlpatterns = [
    path('', DepartmentListView.as_view(), name='organization'),
    path('options/education_level/', edu_level_options, name='edu-level-options'),
    path('add/education_level/', add_education_level, name='add-education-level'),
    path('delete/education_levels/', delete_education_level, name='delete-education-level'),
]