from django.urls import path
from userprofile.views import (
    UserStats, 
    EditProfile, 
    departments, 
    programs, 
    years
)

app_name = 'profile'
urlpatterns = [
    path('<username>/<int:pk>/<str:tab>/', UserStats.as_view(), name='user-stats'),
    path('<username>/<int:pk>/edit/profile', EditProfile.as_view(), name='edit-profile'),
    path('<username>/<int:pk>/edit/departments/', departments, name='department_choices'),
    path('<username>/<int:pk>/edit/programs/', programs, name='program_choices'),
    path('<username>/<int:pk>/edit/years/', years, name='year_choices'),
]

