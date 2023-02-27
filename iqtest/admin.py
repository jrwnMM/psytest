from django.contrib import admin
from .models import Question, Result, Choice, Answer
from django.utils.html import mark_safe
# Register your models here.

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'safe_question')
    search_fields = ('question',)

    def safe_question(self, obj):
        return mark_safe(obj.question.html)
    
class ResultAdmin(admin.ModelAdmin):
    list_display = ('user', 'result')
    search_fields = ('user__user__first_name', 'user__user__last_name',)

class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'question_id', 'safe_choice')
    search_fields = ('choice',)

    def question_id(self,obj):
        return obj.question.id
    
    def safe_choice(self, obj):
        return mark_safe(obj.choice.html)

class AnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'question_id', 'result_id', 'answer_id')
    search_fields = ('answer__choice',)

    def question_id(self,obj):
        return obj.question.id
    def result_id(self,obj):
        return obj.result.id
    def answer_id(self,obj):
        return obj.answer.id


admin.site.register(Question, QuestionAdmin)
admin.site.register(Result, ResultAdmin)
admin.site.register(Choice, ChoiceAdmin)
admin.site.register(Answer, AnswerAdmin)