


from accounts.models import Profile
from administration.models import AdminScheduledConsultation
from datetime import datetime

def get_notif_count(request):
    now = datetime.today()
    context = {}
    if request.user.is_authenticated:
        context["unapproved_users"] = (
            Profile.objects.filter(is_assigned=False)
            .exclude(user__username=request.user or None)
            .count()
        )
        notif_count = (
            AdminScheduledConsultation.objects.filter(
                managed_by__user=request.user or None,
                is_done=False,
                scheduled_date__date=now.date(),
                scheduled_date__time__gt=now.time(),
                user__is_assigned=True,
            ).count()
            + AdminScheduledConsultation.objects.filter(
                managed_by__user=request.user or None,
                is_done=False,
                scheduled_date__lt=now.today(),
                user__is_assigned=True,
            ).count()
        )
        context["notif_count"] = notif_count if notif_count is not None else None

    return context