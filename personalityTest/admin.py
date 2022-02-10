from django.contrib import admin
from .models import Questionnaire, Result,Cluster

# Register your models here.
#admin.site.register(Questionnaire)

@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('user', 'extroversion', 'neurotic', 'agreeable', 'conscientious', 'openness', 'prediction')
    list_filter = ('prediction',)
    search_fields = ('user__first_name', 'user__last_name')

@admin.register(Questionnaire)
class QuestionsAdmin(admin.ModelAdmin):
    list_display = ('question', 'category', 'key')
    list_filter = ('key', 'category')
    prepopulated_fields = {'slug':('question',),}

@admin.register(Cluster)
class ClusterAdmin(admin.ModelAdmin):
    list_display = ('cluster', 'extroversion', 'neurotic', 'agreeable', 'conscientious', 'openness')
    list_editable = ('extroversion', 'neurotic', 'agreeable', 'conscientious', 'openness')