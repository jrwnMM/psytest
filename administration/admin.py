from django.contrib import admin
from .models import AdminScheduledConsultation
# Register your models here.


@admin.register(AdminScheduledConsultation)
class ASCAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'managedby', 'scheduled_date')
    search_fields = ('client__user__first_name', 'client__user__last_name')
    list_filter = ('scheduled_date',)
