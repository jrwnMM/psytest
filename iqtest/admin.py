from django.contrib import admin
from .models import Question, Result, Choice, Answer
# Register your models here.

class QuestionAdmin(admin.ModelAdmin):
    pass
class ResultAdmin(admin.ModelAdmin):
    pass
class ChoiceAdmin(admin.ModelAdmin):
    pass
class AnswerAdmin(admin.ModelAdmin):
    pass

admin.site.register(Question, QuestionAdmin)
admin.site.register(Result, ResultAdmin)
admin.site.register(Choice, ChoiceAdmin)
admin.site.register(Answer, AnswerAdmin)