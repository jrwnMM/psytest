from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin

from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    gender_choices = (
        ('M', 'Male'),
        ('F', 'Female'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=6, choices=gender_choices, null=True, blank=True)
    test_completed = models.DateTimeField(null=True, blank=True)
    is_assigned = models.BooleanField(null=True)
    is_result = models.BooleanField(default=False)
    
    @admin.display(ordering='user__first_name')
    def full_name(self):
        return self.user.get_full_name()

    def __str__(self):
        return self.user.username




@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

