from django.contrib import admin

from .models import RatingQuestion, EssayQuestion, UserFeedback

# Register your models here.

@admin.register(RatingQuestion)
class RatingQuestionAdmin(admin.ModelAdmin):
    list_display = ['question']

@admin.register(EssayQuestion)
class EssayQuestionAdmin(admin.ModelAdmin):
    list_display = ['question']
    

@admin.register(UserFeedback)
class UserFeedbackAdmin(admin.ModelAdmin):
    list_display = ['user']

