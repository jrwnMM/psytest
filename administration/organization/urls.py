from django.urls import path
from .views import (OrganizationView, delete_yearlevel, add_yearlevel, add_education_level, edu_level_options, delete_education_level, delete_department, edu_levels_list_body, add_department, handle_edu_levels_select, department_program_list, add_department_program, delete_program)

urlpatterns = [
    path("", OrganizationView.as_view(), name="organization"),
    path("options/education_level/", edu_level_options, name="edu-level-options"),
    path("list/education_level/", edu_levels_list_body, name="edu-levels-list"),
    path("<int:dept_id>/programs/", department_program_list, name="dept-prog-list"),
    path("add/education_level/", add_education_level, name="add-education-level"),
    path("add_department/", add_department, name="add-department"),
    path("add_department_program/", add_department_program, name="add-department-program"),
    path("add_yearlevel/", add_yearlevel, name="add-yearlevel"),
    path("delete/education_levels/", delete_education_level, name="delete-education-level"),
    path("delete/department/", delete_department, name="delete-department"),
    path("delete/program/", delete_program, name="delete-program"),
    path("delete/yearlevel/", delete_yearlevel, name="delete-yearlevel"),
    path("handle_edu_levels_select/", handle_edu_levels_select, name="handle_edu_levels_select"),
]
