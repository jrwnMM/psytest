from django.contrib import admin
from .models import Question, Answer

# Register your models here.
@admin.register(Question)
class GeneralIQQuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'question')

@admin.register(Answer)
class GeneralIQAnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'answer')
