from django.db import models
from django.db.models.fields import CharField
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Questionnaire(models.Model):

    class Meta:
        verbose_name = _('Questionnaire')
        verbose_name_plural = _('Questionnaires')
        # ordering = ('-id',)

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

    question=models.TextField(editable=True)
    slug=models.SlugField(null=True)
    created = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=100, choices=category_choices)
    key = models.CharField(max_length=10, null=True, blank=True, choices=key_choices)

    def __str__(self):
        return f"{str(self.question)}"

    def save(self,*args, **kwargs):
        self.slug = slugify(self.question)
        return super(Questionnaire, self).save(*args, **kwargs)


class Cluster(models.Model):
    cluster = models.CharField(max_length=10)
    extroversion = models.FloatField(default=0)
    neurotic = models.FloatField(default=0)
    agreeable = models.FloatField(default=0)
    conscientious = models.FloatField(default=0)
    openness = models.FloatField (default=0)

    def __str__(self):
        return self.cluster

class Result(models.Model):
    user=models.OneToOneField(User,null=True, on_delete=models.CASCADE)
    extroversion = models.FloatField(default=0)
    neurotic = models.FloatField(default=0)
    agreeable = models.FloatField(default=0)
    conscientious = models.FloatField(default=0)
    openness = models.FloatField (default=0)
    prediction = models.ForeignKey(Cluster, on_delete=models.CASCADE, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{str(self.user)}"