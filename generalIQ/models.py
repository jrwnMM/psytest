from tokenize import blank_re
from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.
class Question(models.Model):
    question = RichTextUploadingField(blank = True, null = True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"ID: {self.id}"

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.IntegerField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="generaliq_answer_user")