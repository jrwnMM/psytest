from django.urls import path, include
from .views import Home
from .helpers import (
    approve_user,
    delete_career,
    delete_personality,
    unapprove_user,
    send_msg,
    handle_alert,
)

app_name = "administration"

urlpatterns = [
    path("", Home.as_view(), name="home"),
    path("departments/", include("administration.department.urls")),
    path("user-management/", include("administration.usermanagement.urls")),
    path("career/", include("administration.career.urls")),
    path("personality/", include("administration.personality.urls")),
    path("statistics/", include("administration.statistics.urls")),
    path("<username>/send-msg/", send_msg, name="send-msg"),
    path("<int:user_pk>/approve/", approve_user, name="approve-result"),
    path("<int:user_pk>/unapprove/", unapprove_user, name="unapprove-result"),
    path("career/<int:pk>/delete/", delete_career, name="delete-career"),
    path("personality/<int:pk>/delete/", delete_personality, name="delete-personality"),
    path("alert/", handle_alert, name="alert-userschedules"),   

]
