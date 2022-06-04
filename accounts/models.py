from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from dateutil.relativedelta import relativedelta
import datetime
from phonenumber_field.modelfields import PhoneNumberField

class Profile(models.Model):
    gender_choices = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=6, choices=gender_choices, null=True, blank=True)
    contactNumber = PhoneNumberField(unique=True, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    middle_name= models.CharField(max_length=128,null=True, blank=True) #Use custom user model?
    educationlevel = models.ForeignKey("EducationLevel",on_delete=models.SET_NULL,null=True)
    department = models.ForeignKey("Department",on_delete=models.SET_NULL,null=True)
    program= models.ForeignKey("Program",on_delete=models.SET_NULL,null=True)
    year= models.ForeignKey("Year",on_delete=models.SET_NULL,null=True)
    last_test_taken = models.DateTimeField(null=True, blank=True)
    is_assigned = models.BooleanField(null=True)
    is_result = models.BooleanField(null=True)
    
    @admin.display(ordering='user__first_name')
    def full_name(self):
        return self.user.get_full_name()

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

    @property
    def get_age(self):
        if type(self.date_of_birth) is str:
            dob = datetime.datetime.strptime(self.date_of_birth, '%Y-%m-%d')
            return relativedelta(datetime.datetime.today(), dob).years
        elif type(self.date_of_birth) is datetime.date:
            return relativedelta(datetime.datetime.today(), self.date_of_birth).years
        else:
            return None

    def save(self, *args, **kwargs):
        self.age = self.get_age
        super(Profile, self).save(*args, **kwargs)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
        instance.profile.save()

class EducationLevel(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.name

class Department(models.Model):
    educationlevel = models.ForeignKey(EducationLevel, on_delete=models.CASCADE, null=True, blank=True)
    code = models.CharField(max_length=16, null=True, blank=True)
    name = models.CharField(max_length=64, null=True, blank=True)

    def __str__(self):
        return self.name

class Program(models.Model):
    department = models.ForeignKey(Department, on_delete=models.PROTECT, null=True, blank=True, related_name='programs')
    code = models.CharField(max_length=16, null=True, blank=True)
    name = models.CharField(max_length=128, null=True, blank=True)

    def __str__(self):
        return self.name

class Year(models.Model):
    educationlevel = models.ForeignKey(EducationLevel, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(_('Year'),max_length=32, null=True, blank=True)

    def __str__(self):
        return self.name