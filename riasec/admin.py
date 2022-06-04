from django.contrib import admin

from riasec.models import Result,Question, Answer, OfferedProgram
# Register your models here.

@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('id','user', 'realistic', 'investigative', 'artistic', 'social', 'enterprising', 'conventional')
    list_display_links = ('id', 'user',)
    search_fields = ('user__first_name', 'user__last_name')

@admin.register(Question)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'question')
    prepopulated_fields = {'slug':('question',),}

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('user', 'question', 'answer')

@admin.register(OfferedProgram)
class OfferedProgramAdmin(admin.ModelAdmin):
    list_display = ('interest', 'program')