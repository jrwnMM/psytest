from django.urls import path
from .views import (
    TestView, TestContainer
)


app_name = 'personalityTest'
urlpatterns = [
    path('test/', TestView.as_view(), name='test'),
    path('test/submit/', TestView.as_view(), name='submit-test'),
    path('test_container/', TestContainer.as_view(), name='test-container')
]


