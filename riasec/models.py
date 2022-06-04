from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from accounts.models import Program

class Question(models.Model):
    class Meta:
        ordering = ['-id']

    category_choices =[
        ('R','Realistic'),
        ('I','Investigative'),
        ('A','Artistic'),
        ('S','Social'),
        ('E','Enterprising'),
        ('C', 'Conventional'),
    ]
    question=models.TextField(null=True, blank=True)
    slug = models.SlugField(max_length=100, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=100, choices=category_choices)

    def __str__(self):
        return str(self.question)

    def save(self,*args, **kwargs):
            self.slug=slugify(self.question)
            return super(Question, self).save(*args, **kwargs)

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True, blank=True)
    answer = models.IntegerField(null=True, blank=True)
    user = models.ForeignKey(User, models.CASCADE, null=True, blank=True, related_name="career_answer_user")


class Result(models.Model):
    user=models.OneToOneField(User,null=True, on_delete=models.CASCADE, related_name="career_result_user")
    realistic = models.FloatField(default=0)
    investigative = models.FloatField(default=0)
    artistic = models.FloatField(default=0)
    social = models.FloatField(default=0)
    enterprising = models.FloatField (default=0)
    conventional = models.FloatField(default=0)
    date_created = models.DateTimeField(auto_now_add=True)



class OfferedProgram(models.Model):
    class Interest(models.TextChoices):
        REALISTIC = 'realistic', 'Realistic'
        INVESTIGATIVE = 'investigative', 'Investigative'
        ARTISTIC = 'artistic', 'Artistic'
        SOCIAL = 'social', 'Social'
        ENTERPRISING = 'enterprising', 'Enterprising'
        CONVENTIONAL = 'conventional', 'Conventional'
    
    interest = models.CharField(max_length=16, choices=Interest.choices, null=True, blank=True)
    program = models.ForeignKey(Program, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.program}"
    
