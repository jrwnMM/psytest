from django.urls import path
from .views import (
    registerPage,
    loginPage,
    logoutUser,
    activate,
    EditProfile,
    ProfileView
)

app_name='accounts'
urlpatterns = [
    path('register/', registerPage, name='register'),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
    path('login/', loginPage, name='login'),
    path('logout/',logoutUser,name='logout'),
    path('profile/',ProfileView.as_view(), name='profile'),
    path('edit-profile/<int:pk>/', EditProfile.as_view(), name='edit_user'),
]
