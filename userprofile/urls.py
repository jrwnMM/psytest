from django.urls import path
from userprofile.views import (
    UserStats, 
    EditProfile, 
    btn_approve, 
    departments, 
    programs, 
    years
)

app_name = 'profile'
urlpatterns = [
    path('<username>/<int:pk>/', UserStats.as_view(), name='user-stats'),
    path('<username>/<int:pk>/edit/', EditProfile.as_view(), name='edit-profile'),
    path('<username>/<int:pk>/edit/departments/', departments, name='department_choices'),
    path('<username>/<int:pk>/edit/programs/', programs, name='program_choices'),
    path('<username>/<int:pk>/edit/years/', years, name='year_choices'),
    path('<int:pk>/btn-swap/', btn_approve, name='btn-approve'),
]

