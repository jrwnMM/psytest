from django.db import models
from django.contrib import admin
from accounts.models import Profile

# Create your models here.

class AdminScheduledConsultation(models.Model):
    managed_by = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True, related_name='admin_name')
    client = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True, related_name='clients')
    scheduled_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'manage by {self.managed_by.user.username} to {self.client.user.username}'

    @admin.display(ordering='client__user__first_name')
    def full_name(self):
        return self.client.user.get_full_name()

    @admin.display(ordering='managed_by__user__first_name')
    def managedby(self):
        return self.managed_by.user.get_full_name()

    class Meta:
        unique_together = ('managed_by', 'client')