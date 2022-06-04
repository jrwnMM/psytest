from django.urls import path
from .views import DepartmentDetailView, DepartmentListView, addDepartment, addProgram, delete_program, delete_department

urlpatterns = [
    path('', DepartmentListView.as_view(), name='departments'),
    path('<str:code>/details/', DepartmentDetailView.as_view(), name='department-details'),
    path('department/delete/', delete_department, name='delete-department'),
    path('program/delete/', delete_program, name='delete-program'),
    path('add/department/', addDepartment, name='add-department'),
    path('add/program/', addProgram, name='add-program'),
]