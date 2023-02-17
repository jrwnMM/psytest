from django.urls import path
from .views import TestView, TestContainer


app_name = "iqtest"
urlpatterns = [
    path("", TestView.as_view(), name="test"),
    path("test-container/", TestContainer.as_view(), name="test-container"),
]