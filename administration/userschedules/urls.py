from django.urls import path
from .views import (
    UserSchedules,
    MissedSchedules,
    UpcomingSchedules,
    SectionUsers,
    end_session,
    reset_schedule,
)

urlpatterns = [
    path("", UserSchedules.as_view(), name="schedules"),
    path("missed/", MissedSchedules.as_view(), name="missed-schedules"),
    path("upcoming/", UpcomingSchedules.as_view(), name="upcoming-schedules"),
    path("<str:type>/section-users/", SectionUsers.as_view(), name="section-users"),
    path("<int:pk>/<str:type>/end-session/", end_session, name="end-session"),
    path("<int:profile_id>/reset-schedule/", reset_schedule, name="reset-schedule"),
]
