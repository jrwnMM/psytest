from django.contrib import admin
from .models import AdminScheduledConsultation
# Register your models here.


@admin.register(AdminScheduledConsultation)
class ASCAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'managedby', 'scheduled_date', 'is_done')
    search_fields = ('user__user__first_name', 'user__user__last_name')
    list_filter = ('is_done', 'scheduled_date')
