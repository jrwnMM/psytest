from django.urls import path
from .views import (
    Statistics,
    IQStats,
    career_category, 
    career_college, 
    career_grade, 
    career_junior, 
    career_male, 
    career_female, 
    career_senior,
    personality_college, 
    personality_grade, 
    personality_junior, 
    personality_male, 
    personality_female, 
    personality_senior,
    personality_category
)

urlpatterns = [
    path('', Statistics.as_view(), name="statistics"),
    path('iq_stats/', IQStats.as_view(), name="iq-stats"),
    path('career_male/', career_male, name="career_male"),
    path('career_female/', career_female, name="career_female"),
    path('career_college/', career_college, name="career_college"),
    path('career_senior/', career_senior, name="career_senior"),
    path('career_junior/', career_junior, name="career_junior"),
    path('career_grade/', career_grade, name="career_grade"),
    path('career_category/', career_category, name="statistics_career_category"),
    path('personality_male/', personality_male, name="personality_male"),
    path('personality_female/', personality_female, name="personality_female"),
    path('personality_college/', personality_college, name="personality_college"),
    path('personality_senior/', personality_senior, name="personality_senior"),
    path('personality_junior/', personality_junior, name="personality_junior"),
    path('personality_grade/', personality_grade, name="personality_grade"),
    path('personality_category/', personality_category, name="statistics_personality_category"),
]