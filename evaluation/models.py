from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class RatingQuestion(models.Model):
    question = models.CharField(max_length=256, null=True, blank=True)
    pub_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question
    
class EssayQuestion(models.Model):
    question = models.CharField(max_length=256, null=True, blank=True)
    pub_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question

class UserFeedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    q_1 = models.PositiveIntegerField(null=True, blank=True)
    q_2 = models.PositiveIntegerField(null=True, blank=True)
    q_3 = models.PositiveIntegerField(null=True, blank=True)
    q_4 = models.PositiveIntegerField(null=True, blank=True)
    q_5 = models.PositiveIntegerField(null=True, blank=True)
    q_6 = models.PositiveIntegerField(null=True, blank=True)
    q_7 = models.PositiveIntegerField(null=True, blank=True)
    q_8 = models.PositiveIntegerField(null=True, blank=True)

    e_1 = models.TextField(null=True, blank=True)
    e_2 = models.TextField(null=True, blank=True)
    e_3 = models.TextField(null=True, blank=True)
    e_4 = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.user.username
    
