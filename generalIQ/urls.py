from django.urls import path
from . import views

app_name = "generaliq"
urlpatterns = [
    path("", views.generalIQTest, name="generalIQTest"),
]