from accounts.models import Profile
from administration.models import AdminScheduledConsultation
from datetime import datetime


def get_obj_count(request):
    now = datetime.today()
    context = {}
    if request.user.is_authenticated:
        is_result = (Profile.objects.filter(is_result=False)
                .exclude(user__username=request.user.username)
                .count())
        is_assigned_false = (Profile.objects.filter(is_assigned=False)
                .exclude(user__username=request.user.username)
                .count())

        active_session_count = AdminScheduledConsultation.objects.exclude(
                managed_by__user__username=request.user.username
            ).count()

        notif_count = (
        AdminScheduledConsultation.objects.filter(
            managed_by__user=request.user,
            scheduled_date__date=now.date(),
            scheduled_date__time__gt=now.time(),
            client__is_assigned=True,
        ).count()
        + AdminScheduledConsultation.objects.filter(
            managed_by__user=request.user,
            scheduled_date__lt=now.today(),
            client__is_assigned=True,
        ).count()
)
    
        context["userstocheck"] = is_result + is_assigned_false
        context["notif_count"] = notif_count if notif_count is not None else None
        context["pending_results_count"] = is_result
        context["active_sessions_count"] = active_session_count
        context["counseling_requests_count"] = is_assigned_false

    return context
