from django.db import models
from accounts.models import Profile

# Create your models here.

class AdminScheduledConsultation(models.Model):
    managed_by = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True, related_name='admin_name')
    user = models.OneToOneField(Profile, on_delete=models.CASCADE, null=True, blank=True, related_name='clients')
    # approved_time = models.DateTimeField(null=True, blank=True)
    scheduled_date = models.DateTimeField(null=True, blank=True)
    is_done = models.BooleanField(default=False)

    def __str__(self):
        return f'manage by {self.managed_by.user.username} to {self.user.user.username}'

