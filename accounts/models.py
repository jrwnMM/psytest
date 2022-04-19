from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver
from dateutil.relativedelta import relativedelta
from datetime import datetime
from phonenumber_field.modelfields import PhoneNumberField



class Department(models.Model):
    department=[
        ('IBED','Integrated Basic Education (Preschool to SHS)'),
        ('College','College Department')
    ]

    name = models.CharField(_('Department'),max_length=50,choices=department)

    def __str__(self):
        return self.name


class Program(models.Model):
    programs = [
        ('Grade', 'Grade School'),
        ('Junior', 'Junior Highschool'),
        ('Senior', 'Senior Highschool'),
        ('BSA', 'BS in Accountancy'),
        ('BSBA', 'BS in Business Administration'),
        ('BSMA', 'BS in Management Accounting'),
        ('BSC', 'BS in Criminology'),
        ('BSCE', 'BS in Civil Engineering'),
        ('BSE', 'Bachelor in Secondary Education'),
        ('BEE', 'Bachelor in Elementary Education'),
        ('BSIT', 'BS in Information Technology'),
        ('BSP', 'BS in Psychology'),
        ('BSSW', 'BS in Social Work'),
        ('BSMT', 'BS in Medical Technology'),
    ]

    name = models.CharField(_('Program'),max_length=50,choices=programs)
    department = models.ForeignKey(Department,on_delete=models.CASCADE)
    def __str__(self):
        return self.name

class Year(models.Model):
    year=[
        ('1','Grade 1'),
        ('2','Grade 2'),
        ('3','Grade 3'),
        ('4','Grade 4'),
        ('5','Grade 5'),
        ('6','Grade 6'),
        ('7','Grade 7'),
        ('8','Grade 8'),
        ('9','Grade 9'),
        ('10','Grade 10'),
        ('11','Grade 11'),
        ('12','Grade 12'),
        ('1st','1st Year'),
        ('2nd','2nd Year'),
        ('3rd','3rd Year'),
        ('4th','4th Year'),
        ('5th','5th Year'),
    ]

    name = models.CharField(_('Year'),max_length=10,choices=year)

    def __str__(self):
        return self.name

class Profile(models.Model):
    gender_choices = (
        ('M', 'Male'),
        ('F', 'Female'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=6, choices=gender_choices, null=True, blank=True)
    #added models---------------
    contacts = PhoneNumberField(unique=True, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    middle_name= models.CharField(max_length=128,null=True, blank=True) #Use custom user model?
    #add fields in filters.py
    #---------------------------
    department = models.ForeignKey(Department,on_delete=models.SET_NULL,null=True)
    program= models.ForeignKey(Program,on_delete=models.SET_NULL,null=True)
    year= models.ForeignKey(Year,on_delete=models.SET_NULL,null=True)
    test_completed = models.DateTimeField(null=True, blank=True)
    is_assigned = models.BooleanField(null=True)
    is_result = models.BooleanField(default=False)
    
    @admin.display(ordering='user__first_name')
    def full_name(self):
        return self.user.get_full_name()

    def __str__(self):
        return self.user.username

#get_age----------------
    @property
    def get_age(self):
        if self.date_of_birth:
            return relativedelta(datetime.today(), self.date_of_birth).years
        else:
            return None
#save_age---------------
    def save(self, *args, **kwargs):
        self.age = self.get_age
        super(Profile, self).save(*args, **kwargs)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
        instance.profile.save()

