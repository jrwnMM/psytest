from django.contrib import admin
from .models import Riasec_result,RIASEC_Test
# Register your models here.

@admin.register(Riasec_result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('id','user', 'realistic', 'investigative', 'artistic', 'social', 'enterprising', 'conventional')
    list_display_links = ('id', 'user',)
    search_fields = ('user__first_name', 'user__last_name')


@admin.register(RIASEC_Test)
class AuthorAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('question',),}