from django.urls import path
from .views import Home, ResultPage
from . import views

app_name='riasec'
urlpatterns = [
    path('test/', views.testPage, name='test'),
    path('home/', Home.as_view(), name='home'),
    path('result/', ResultPage.as_view(), name='result'),
    path('test/evaluate/', views.evaluate, name='test_evaluate'),
]
