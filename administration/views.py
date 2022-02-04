from django.contrib.auth.models import User
from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import ObjectDoesNotExist
from django.http import request
from django.http.response import Http404, HttpResponseBadRequest, HttpResponseRedirect
from django.urls.base import reverse
from django.views.generic import (
    TemplateView,
    ListView,
    UpdateView,
    DetailView,
    CreateView,
    DeleteView,
)
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin,
    PermissionRequiredMixin,
)
from django.views.generic import View
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic.edit import FormMixin

from personalityTest.models import Questionnaire, Result
from psytests.forms import ContactForm
from riasec.models import RIASEC_Test, Riasec_result

from datetime import datetime

from .forms import ScheduleDateForm, SearchForm, AddRQuestionsForm, AddPQuestionsForm
from .models import AdminScheduledConsultation

from accounts.models import Profile
from accounts.forms import UpdateUserForm

from django.core.mail import send_mail
from django.conf import settings

now = datetime.today()

# Create your views here.
class SuperUserCheck(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["unapproved_users"] = (
            Profile.objects.filter(is_assigned=False)
            .exclude(user__username=self.request.user)
            .count()
        )
        notif_count = (
            AdminScheduledConsultation.objects.filter(
                managed_by__user=self.request.user,
                is_done=False,
                scheduled_date__date=now.date(),
                scheduled_date__time__gt=now.time(),
                user__is_assigned=True,
            ).count()
            + AdminScheduledConsultation.objects.filter(
                managed_by__user=self.request.user,
                is_done=False,
                scheduled_date__lt=now.today(),
                user__is_assigned=True,
            ).count()
        )
        context["notif_count"] = notif_count if notif_count is not None else None

        return context


class UserAccessMixin(PermissionRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect_to_login(
                self.request.get_full_path(),
                self.get_login_url(),
                self.get_redirect_field_name(),
            )
        if not self.has_permission():
            return redirect("")
        return super(UserAccessMixin, self).dispatch(request, *args, **kwargs)


class Home(LoginRequiredMixin, SuperUserCheck, TemplateView):
    template_name = "administration/admin_home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context


class UserManagement(LoginRequiredMixin, SuperUserCheck, ListView):
    template_name = "administration/user_management.html"
    model = User
    context_object_name = "users"
    paginate_by = 8

    def get_queryset(self):
        query = self.request.GET.get("name")
        if query:
            object_list = self.model.objects.filter(username__icontains=query).exclude(
                username=self.request.user
            )
        else:
            object_list = self.model.objects.exclude(username=self.request.user)
        return object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = SearchForm
        context["users_total"] = self.get_queryset().count()

        return context


class UserDetailUpdate(LoginRequiredMixin, SuperUserCheck, UpdateView):
    template_name = "administration/user_detail_update.html"
    model = User
    form_class = UpdateUserForm
    success_url = reverse_lazy("administration:user-management")


class PendingUsers(LoginRequiredMixin, SuperUserCheck, ListView):
    template_name = "administration/pending-users.html"
    model = Profile
    context_object_name = "users"
    paginate_by = 4

    def get_queryset(self):
        query = self.request.GET.get("name")
        if query:
            object_list = (
                self.model.objects.filter(
                    user__username__icontains=query, is_assigned=False
                )
                .order_by("is_assigned")
                .exclude(user__username=self.request.user)
            )
        else:
            obj_excluded = self.model.objects.exclude(user__username=self.request.user)
            object_list = obj_excluded.filter(is_assigned=False)
        return object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = SearchForm
        context["users_pending"] = (
            Profile.objects.filter(is_assigned=False)
            .exclude(user__username=self.request.user)
            .count()
        )
        context["users_assigned"] = (
            AdminScheduledConsultation.objects.filter(user__is_assigned=True)
            .exclude(managed_by=Profile.objects.get(user__username=self.request.user))
            .count()
        )
        return context


class AssignedUsers(LoginRequiredMixin, SuperUserCheck, ListView):
    template_name = "administration/assigned-users.html"
    model = AdminScheduledConsultation
    context_object_name = "users"
    paginate_by = 4

    def get_queryset(self):
        query = self.request.GET.get("name")
        if query:
            object_list = self.model.objects.filter(
                user__user__username__icontains=query, user__is_assigned=True
            ).exclude(user__user__username=self.request.user)
        else:
            obj = Profile.objects.get(user__username=self.request.user)
            obj_excluded = self.model.objects.exclude(managed_by=obj)
            object_list = obj_excluded.filter(user__is_assigned=True)
        return object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = SearchForm
        context["users_assigned"] = (
            AdminScheduledConsultation.objects.filter(user__is_assigned=True)
            .exclude(managed_by=Profile.objects.get(user__username=self.request.user))
            .count()
        )
        context["users_pending"] = (
            Profile.objects.filter(is_assigned=False)
            .exclude(user__username=self.request.user)
            .count()
        )
        return context

class UserDetailViewMixin(UserPassesTestMixin):
    
    def test_func(self):
        obj = get_object_or_404(Profile, user__username = self.request.user)
        
        if obj.user.is_superuser:
            test = True
            if obj.user.username == self.kwargs['user']:
                if obj.is_result == False:
                    test = False
        elif obj.is_result:
            if obj.user.username == self.kwargs['user']: 
                test = True
            else: 
                test = False
        else:
            test = False
        return test
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["unapproved_users"] = (
            Profile.objects.filter(is_assigned=False)
            .exclude(user__username=self.request.user)
            .count()
        )
        notif_count = (
            AdminScheduledConsultation.objects.filter(
                managed_by__user=self.request.user,
                is_done=False,
                scheduled_date__date=now.date(),
                scheduled_date__time__gt=now.time(),
                user__is_assigned=True,
            ).count()
            + AdminScheduledConsultation.objects.filter(
                managed_by__user=self.request.user,
                is_done=False,
                scheduled_date__lt=now.today(),
                user__is_assigned=True,
            ).count()
        )
        context["notif_count"] = notif_count if notif_count is not None else None

        return context

class UserDetailView(LoginRequiredMixin, UserDetailViewMixin, FormMixin, DetailView):
    template_name = "stats/stats.html"
    model = User
    form_class = ContactForm
    context_object_name = "user"

    def get_success_url(self):
        return reverse_lazy(
            "administration:user_detail",
            kwargs={"user": self.kwargs["user"], "pk": self.kwargs["pk"]},
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            obj = Profile.objects.get(user__username=self.kwargs.get("user"))
            context["profile"] = obj
        except:
            pass

        try:
            obj = AdminScheduledConsultation.objects.get(
                user__user__username=self.kwargs.get("user")
            )
            context["admin"] = obj
            if obj.is_done == True:
                context["done"] = obj.is_done
            if obj.scheduled_date:
                context["scheduled"] = obj.scheduled_date
        except:
            pass

        try:
            context["riasec_result"] = Riasec_result.objects.get(
                user__username=self.kwargs.get("user"), user__id=self.kwargs.get("pk")
            )
            obj = (
                Riasec_result.objects.filter(
                    user__username=self.kwargs.get("user"),
                    user__id=self.kwargs.get("pk"),
                )
                .values(
                    "realistic",
                    "investigative",
                    "artistic",
                    "social",
                    "enterprising",
                    "conventional",
                )
                .first()
            )
            if obj is not None:
                objects = dict(
                    sorted(obj.items(), key=lambda item: item[1], reverse=True)
                )
                top1 = {}
                top2 = {}
                top3 = {}
                for x in objects:
                    if not top1:
                        top1[x] = objects[x]
                    else:
                        if objects[x] == list(top1.values())[0]:
                            top1[x] = objects[x]
                        if top2:
                            if objects[x] < list(top2.values())[0] and not top3:
                                top3[x] = objects[x]
                                continue
                        if objects[x] < list(top1.values())[0] and not top3:
                            top2[x] = objects[x]
                        if top3:
                            if objects[x] == list(top3.values())[0]:
                                top3[x] = objects[x]
                context["top1"] = top1
                context["top1len"] = range(len(top1))
                context["top2"] = top2
                context["top2len"] = range(len(top2))
                context["top3"] = top3
                context["top3len"] = range(len(top3))
                if top1:
                    context["top1value"] = list(top1.values())[0]
                if top2:
                    context["top2value"] = list(top2.values())[0]
                if top3:
                    context["top3value"] = list(top3.values())[0]
        except ObjectDoesNotExist:
            pass

        try:
            context["personalityTest_result"] = Result.objects.get(
                user__username=self.kwargs.get("user"), user__id=self.kwargs.get("pk")
            )
            obj_prediction = Result.objects.get(
                user__username=self.kwargs.get("user"), user__id=self.kwargs.get("pk")
            )
            context["prediction"] = obj_prediction.prediction
        except ObjectDoesNotExist:
            pass

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        obj = Profile.objects.get(user__username=self.kwargs["user"])
        subject = self.request.POST.get("subject")
        message = self.request.POST.get("message")
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [
            obj.user.email,
        ]
        send_mail(subject, message, email_from, recipient_list, fail_silently=True)
        return super().form_valid(form)

def send_msg(request, user):
        obj = Profile.objects.get(user__username=user)
        subject = request.POST.get("subject")
        message = request.POST.get("message")
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [
            obj.user.email,
        ]
        send_mail(subject, message, email_from, recipient_list, fail_silently=True)
        return redirect('administration:pending-users')

def return_user(request, user, pk):
    try:
        admin = AdminScheduledConsultation.objects.get(user__user__username=user)
        admin.delete()
    except ObjectDoesNotExist:
        pass

    try:
        profile = Profile.objects.get(user__username=user)
        profile.is_assigned = False
        profile.is_result = False
        profile.save()
    except:
        pass

    return redirect("administration:pending-users")

def approve_user(request, user, pk):
    try:
        admin = AdminScheduledConsultation.objects.get(user__user__username=user)
        admin.is_done = True
        admin.scheduled_date = None
        admin.save()
    except ObjectDoesNotExist:
        user_obj = Profile.objects.get(user__username=user)
        managed_by = Profile.objects.get(user__username=request.user)
        admin = AdminScheduledConsultation(
            user=user_obj, managed_by=managed_by, is_done=True
        )
        admin.save()

    try:
        profile = Profile.objects.get(user__username=user)
        profile.is_assigned = None
        profile.is_result = True
        profile.save()
    except:
        pass

    obj = Profile.objects.get(user__username=user)
    print(request.GET.get('user'), 'Print User' )
    subject = 'Well done!'
    message = f'Your result is now available. Go to the app > Assessment > View Result or go directly here http://jmcproject.herokuapp.com/administration/stats/{user}/{pk}/'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [
        obj.user.email,
    ]
    send_mail(subject, message, email_from, recipient_list, fail_silently=True)

    return redirect("administration:history-schedules")


def deleteRecord(request, p_pk, p_user, r_pk, r_user):
    try:
        if p_user:
            obj = Profile.objects.get(user__username=p_user)
        else:
            obj = Profile.objects.get(user__username=r_user)

        try:
            obj2 = AdminScheduledConsultation.objects.get(user=obj)
            obj2.delete()
        except:
            pass
        
        obj.is_assigned = None
        obj.is_result = False
        obj.save()
    except ObjectDoesNotExist:
        pass

    r = get_object_or_404(Riasec_result, pk=r_pk, user__username=r_user)
    r.delete()

    p = get_object_or_404(Result, pk=p_pk, user__username=p_user)
    p.delete()

    messages.success(request, "record has been deleted")
    return redirect("homepage")


class RQuestionsTemplateView(SuperUserCheck, ListView):
    model = RIASEC_Test
    template_name = "administration/questions/rquestions.html"
    context_object_name = 'rquestions'
    paginate_by = 10


class PQuestionsTemplateView(SuperUserCheck, ListView):
    model = Questionnaire
    template_name = "administration/questions/pquestions.html"
    context_object_name = 'pquestions'
    paginate_by = 10



class RQuestionsCreateView(UserAccessMixin, CreateView):
    permission_required = "can_create"
    model = RIASEC_Test
    form_class = AddRQuestionsForm
    template_name = "administration/questions/rquestions_add.html"
    success_url = reverse_lazy("administration:rquestions")

    def form_valid(self, form):
        return super(RQuestionsCreateView, self).form_valid(form)


class PQuestionsCreateView(UserAccessMixin, CreateView):
    permission_required = "can_create"
    model = Questionnaire
    form_class = AddPQuestionsForm
    template_name = "administration/questions/pquestions_add.html"
    success_url = reverse_lazy("administration:pquestions")

    def form_valid(self, form):
        return super(PQuestionsCreateView, self).form_valid(form)


class RQuestionsEditView(UserAccessMixin, UpdateView):
    permission_required = "can_edit"
    model = RIASEC_Test
    form_class = AddRQuestionsForm
    template_name = "administration/questions/rquestions_add.html"
    success_url = reverse_lazy("administration:rquestions")


class PQuestionsEditView(UserAccessMixin, UpdateView):
    permission_required = "can_edit"
    model = Questionnaire
    form_class = AddPQuestionsForm
    template_name = "administration/questions/pquestions_add.html"
    success_url = reverse_lazy("administration:pquestions")


class RDeleteQuestions(UserAccessMixin, DeleteView):
    permission_required = "can_delete"
    model = RIASEC_Test
    success_message = "question deleted successfully."
    success_url = reverse_lazy("administration:rquestions")

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(RDeleteQuestions, self).delete(request, *args, **kwargs)


class PDeleteQuestions(UserAccessMixin, DeleteView):
    permission_required = "can_delete"
    model = Questionnaire
    success_message = "question deleted successfully."
    success_url = reverse_lazy("administration:pquestions")

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(PDeleteQuestions, self).delete(request, *args, **kwargs)


class UserSchedules(LoginRequiredMixin, SuperUserCheck, ListView):
    template_name = "administration/schedules/schedules.html"
    model = AdminScheduledConsultation
    context_object_name = "users"
    paginate_by = 8

    def get_queryset(self):
        object_list = AdminScheduledConsultation.objects.filter(
            managed_by__user=self.request.user, is_done=False
        )

        return object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()
        soon = queryset.filter(
            scheduled_date__date=now.date(),
            scheduled_date__time__gt=now.time(),
            user__is_assigned=True,
        )
        upcoming = queryset.filter(
            scheduled_date__date__gt=now.date(), user__is_assigned=True
        )
        late = queryset.filter(scheduled_date__lt=now.today(), user__is_assigned=True)
        history = AdminScheduledConsultation.objects.filter(
            managed_by__user=self.request.user, is_done=True
        )
        context["users"] = soon
        context["user_count"] = soon.count()
        context["late"] = late
        context["late_count"] = late.count()
        context["upcoming"] = upcoming
        context["upcoming_count"] = upcoming.count()

        context["history"] = history

        return context


class MissedSchedules(UserSchedules):
    template_name = "administration/schedules/missed.html"


class UpcomingSchedules(UserSchedules):
    template_name = "administration/schedules/upcoming.html"


class HistorySchedules(UserSchedules):
    template_name = "administration/schedules/history.html"


class ResetSchedule(LoginRequiredMixin, SuperUserCheck, UpdateView):
    template_name = "administration/schedules/reset_schedule.html"
    model = AdminScheduledConsultation
    form_class = ScheduleDateForm
    success_url = reverse_lazy("administration:schedules")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = AdminScheduledConsultation.objects.get(id=self.kwargs["pk"])
        return context

    def get_initial(self):
        initial = super().get_initial()
        initial["is_done"] = False
        return initial

    def form_valid(self, form):
        form.save()
        obj = AdminScheduledConsultation.objects.get(id=self.kwargs["pk"])
        target = Profile.objects.get(user__username=obj.user.user.username)
        target.is_assigned = True
        target.save()

        subject = 'Schedule Reset'
        message = f'Hello, there have been changes in schedule. Your new consultation time will be followed on {obj.scheduled_date.strftime("%d %B, %Y  %H:%M%p")}'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [
            target.user.email,
        ]
        send_mail(subject, message, email_from, recipient_list, fail_silently=True)

        return super().form_valid(form)


class SetSchedule(LoginRequiredMixin, SuperUserCheck, CreateView):
    template_name = "administration/schedules/set_date.html"
    model = AdminScheduledConsultation
    form_class = ScheduleDateForm
    success_url = reverse_lazy("administration:pending-users")

    def get_initial(self):
        initial = super().get_initial()
        initial["managed_by"] = Profile.objects.get(user__username=self.request.user)
        initial["user"] = Profile.objects.get(user__username=self.kwargs["username"])
        initial["is_done"] = False

        return initial

    def form_valid(self, form):
        form.save()
        obj = Profile.objects.get(user__username=self.kwargs["username"])
        obj_x = AdminScheduledConsultation.objects.get(user=obj)
        obj.is_assigned = True
        obj.save()
        
        subject = 'Consultation Notice'
        message = f'Hello, you are asked to report in guidance office for consultation. Your schedule is set to {obj_x.scheduled_date.strftime("%d %B, %Y  %H:%M%p")}'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [
            obj.user.email,
        ]
        send_mail(subject, message, email_from, recipient_list, fail_silently=True)

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = Profile.objects.get(user__username=self.kwargs["username"])
        return context
