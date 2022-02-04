from django.urls import path
from .views import (
    TestView,
)


app_name = 'personalityTest'
urlpatterns = [
    path('test/', TestView.as_view(), name='test'),
]


