from django.urls import path
from .views import EvaluationView


app_name = 'evaluation'
urlpatterns = [
    path('', EvaluationView.as_view(), name='view')
]