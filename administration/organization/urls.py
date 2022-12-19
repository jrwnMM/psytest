from django.urls import path
from .views import (OrganizationView, add_education_level, edu_level_options, delete_education_level, edu_levels_list_body, add_department,handle_edu_levels_select)

urlpatterns = [
    path('', OrganizationView.as_view(), name='organization'),
    path('options/education_level/', edu_level_options, name='edu-level-options'),
    path('list/education_level/', edu_levels_list_body, name='edu-levels-list'),
    path('add/education_level/', add_education_level, name='add-education-level'),
    path('add/department/', add_department, name='add-department'),
    path('delete/education_levels/', delete_education_level, name='delete-education-level'),
    path('handle_edu_levels_select/', handle_edu_levels_select, name="handle_edu_levels_select")
]