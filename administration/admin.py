from django.contrib import admin
from .models import AdminScheduledConsultation
# Register your models here.

class ASCAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'managed_by', 'scheduled_date', 'is_done']

admin.site.register(AdminScheduledConsultation, ASCAdmin)