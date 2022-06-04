from django.urls import path
from .views import GetQuestions, PersonalityView, add_question, delete_question, update_question

urlpatterns = [
    path('', PersonalityView.as_view(), name='personality'),
    path('get-questions/', GetQuestions.as_view(), name='get-personality-questions'),
    path('add/question/', add_question, name='add-personality-question'),
    path('delete/question/', delete_question, name='delete-personality-question'),
    path('update/question/<int:pk>', update_question, name='update-personality-question')
]