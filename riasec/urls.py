from django.urls import path
from . import views

app_name='riasec'
urlpatterns = [
    path('test/', views.testPage, name='test'),
    path('test/evaluate/', views.evaluate, name='test_evaluate'),
]
