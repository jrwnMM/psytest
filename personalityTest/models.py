from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from riasec.models import OfferedProgram

# Create your models here.
class Question(models.Model):
    class Meta:
        ordering = ['-id']

    category_choices =[
        ('EXT','Extroversion'),
        ('EST','Neurotic'),
        ('AGR','Agreeable'),
        ('CSN','Conscientious'),
        ('OPN','Openness'),
    ]

    key_choices = [
        ('1', 'Positive'),
        ('0', 'Negative')
    ]
    question=models.TextField(null=True, blank=True)
    slug=models.SlugField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=100, choices=category_choices)
    key = models.CharField(max_length=10, null=True, blank=True, choices=key_choices)

    def __str__(self):
        return f"{str(self.question)}"

    def save(self,*args, **kwargs):
        self.slug = slugify(self.question)
        return super(Question, self).save(*args, **kwargs)

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.SET_NULL, null=True, blank=True)
    answer = models.IntegerField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="personality_answer_user")

class Result(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="personality_result_user")
    extroversion = models.FloatField(default=0)
    neurotic = models.FloatField(default=0)
    agreeable = models.FloatField(default=0)
    conscientious = models.FloatField(default=0)
    openness = models.FloatField (default=0)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{str(self.user)}"


class RecommendedProgram(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    offeredProgram = models.ForeignKey(OfferedProgram, on_delete=models.PROTECT, null=True, blank=True)