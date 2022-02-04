from django.contrib import admin
from .models import Riasec_result,RIASEC_Test
# Register your models here.

class ResultAdmin(admin.ModelAdmin):
    list_display = ['id','user', 'realistic', 'investigative', 'artistic', 'social', 'enterprising', 'conventional']
    list_filter = ['user']

admin.site.register(Riasec_result, ResultAdmin)

@admin.register(RIASEC_Test)
class AuthorAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('question',),}