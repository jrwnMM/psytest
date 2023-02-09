from django.urls import path
from .views import IQView, add_question, add_choice, delete_choice, delete_question, update_question_view, update_question_form

urlpatterns = [ 
    path('', IQView.as_view(), name='manage_iq'),
    path('add/question/', add_question, name='add-iq-question'),
    path('delete/question/', delete_question, name='delete-iq-question'),
    path('update/question/view', update_question_view, name='update-iq-question-view'),
    path('update/question/form', update_question_form, name='update-iq-question-form'),
    path("add_choice/", add_choice, name="add-choice"),
    path("delete/<int:id>/<int:question_id>/", delete_choice, name='delete-choice'),
]