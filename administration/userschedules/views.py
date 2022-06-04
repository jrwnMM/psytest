from django.contrib import messages
from django.http import HttpResponse
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import user_passes_test
from django_htmx.http import trigger_client_event
from datetime import datetime
from accounts.models import Profile
from administration.models import AdminScheduledConsultation
from administration.views import SuperUserCheck


class UserSchedules(LoginRequiredMixin, SuperUserCheck, ListView):
    template_name = "userschedules/schedules.html"
    model = AdminScheduledConsultation
    context_object_name = "users"
    paginate_by = 8

    def get_queryset(self):
        now = datetime.today()
        object_list = AdminScheduledConsultation.objects.filter(
            managed_by__user=self.request.user
            ).filter(
            scheduled_date__date=now.date(),
            scheduled_date__time__gt=now.time(),
            client__is_assigned=True,
        )
        return object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["type"] = "today"
        context['title'] = "Today's"
        context['no_record'] = "No record of appointments for today"
        return context

class MissedSchedules(LoginRequiredMixin, SuperUserCheck, ListView):
    template_name = "userschedules/schedules.html"
    model = AdminScheduledConsultation
    context_object_name = "users"
    paginate_by = 8

    def get_queryset(self):
        now = datetime.today()
        object_list = AdminScheduledConsultation.objects.filter(
            managed_by__user=self.request.user
            ).filter(scheduled_date__lt=now.today(), client__is_assigned=True)
        return object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["type"] = "missed"
        context['title'] = "Missed"
        context['no_record'] = "No record of missed schedules"

        return context


class UpcomingSchedules(LoginRequiredMixin, SuperUserCheck, ListView):
    template_name = "userschedules/schedules.html"
    model = AdminScheduledConsultation
    context_object_name = "users"
    paginate_by = 8

    def get_queryset(self):
        now = datetime.today()
        object_list = AdminScheduledConsultation.objects.filter(
            managed_by__user=self.request.user
            ).filter(
            scheduled_date__date__gt=now.date(), client__is_assigned=True
        )
        return object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["type"] = "upcoming"
        context['title'] = "Upcoming"
        context['no_record'] = "No record of upcoming schedules"

        return context

class SectionUsers(LoginRequiredMixin, SuperUserCheck, ListView):
    template_name = 'userschedules/partials/section-users.html'
    model = AdminScheduledConsultation
    context_object_name = "users"
    paginate_by = 8

    def get_queryset(self):         
        now = datetime.today()

        if self.kwargs['type'] == 'today':
            object_list = AdminScheduledConsultation.objects.filter(
            managed_by__user=self.request.user
            ).filter(
            scheduled_date__date=now.date(),
            scheduled_date__time__gt=now.time(),
            client__is_assigned=True)

        elif self.kwargs['type'] == 'missed':
            object_list = AdminScheduledConsultation.objects.filter(
            managed_by__user=self.request.user
            ).filter(scheduled_date__lt=now.today(), client__is_assigned=True)

        elif self.kwargs['type'] == 'upcoming':
            object_list = AdminScheduledConsultation.objects.filter(
                managed_by__user=self.request.user
                ).filter(scheduled_date__date__gt=now.date(), client__is_assigned=True)

        return object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["type"] = self.kwargs['type']
        if self.kwargs['type'] == 'today':
            context['title'] = "Today's"
            context['no_record'] = "No record of appointment for today"
        elif self.kwargs['type'] == 'missed':
            context['title'] = "Missed"
            context['no_record'] = "No record of missed schedules"
        elif self.kwargs['type'] == 'upcomming':
            context['title'] = "Upcoming"
            context['no_record'] = "No record of upcoming schedules"

        return context
        
@user_passes_test(lambda u:u.is_superuser)        
def end_session(request, pk, type):
    profile = Profile.objects.get(id=pk)
    profile.is_assigned = None
    profile.save()

    sched = AdminScheduledConsultation.objects.filter(client=profile)
    sched.delete()

    messages.success(request, 'Successfully ended', extra_tags='success')
    response = HttpResponse('')
    trigger_client_event(response, 'alert', {})
    trigger_client_event(response, 'refresh_users', {})
    return response

@user_passes_test(lambda u:u.is_superuser)        
def reset_schedule(request, profile_id):
    client = Profile.objects.get(id=profile_id)
    managed_by = Profile.objects.get(id=request.POST['managed_by'])
    sched = AdminScheduledConsultation.objects.filter(managed_by = managed_by, client = client)

    if sched.exists():
        sched.update(scheduled_date = request.POST['scheduled_date'])
        messages.success(request, 'successfully updated', extra_tags='success')
    else:
        new_sched = AdminScheduledConsultation()
        new_sched.managed_by = managed_by
        new_sched.client = client
        new_sched.scheduled_date = request.POST['scheduled_date']
        new_sched.save()
        client.is_assigned = True
        client.save()
        messages.success(request, 'successfully booked', extra_tags='success')

    response = HttpResponse('')
    trigger_client_event(response, 'alert', {})
    trigger_client_event(response, 'refresh_users', {})
    return response


