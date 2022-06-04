from django.contrib import admin
from .models import Answer, Question, RecommendedProgram, Result

# Register your models here.
#admin.site.register(Questionnaire)

@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'extroversion', 'neurotic', 'agreeable', 'conscientious', 'openness')
    search_fields = ('user__first_name', 'user__last_name')

@admin.register(Question)
class QuestionsAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'category', 'key')
    list_filter = ('key', 'category')
    prepopulated_fields = {'slug':('question',),}
    
@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('user', 'question', 'answer')

@admin.register(RecommendedProgram)
class RecommendedProgramAdmin(admin.ModelAdmin):
    list_display = ('user', 'offeredProgram')