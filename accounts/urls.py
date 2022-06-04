from django.urls import path
from .views import (
    departments,
    registerPage,
    loginPage,
    logoutUser,
    activate,
    years,
    programs,
)

app_name='accounts'
urlpatterns = [
    path('register/', registerPage, name='register'),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
    path('login/', loginPage, name='login'),
    path('logout/',logoutUser,name='logout'),
    path('register/departments/', departments, name='department_choices'),
    path('register/programs/', programs, name='program_choices'),
    path('register/years/', years, name='year_choices'),

]
