from django.urls import path
from .views import UserManagement, makesuperuser, unsuperuser

urlpatterns = [
    path('', UserManagement.as_view(), name='user-management'),
    path('<int:pk>/makesuperuser', makesuperuser, name='makesuperuser'),
    path('<int:pk>/unsuperuser', unsuperuser, name='unsuperuser'),
]