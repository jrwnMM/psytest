from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404, redirect
from django.views.generic.base import RedirectView, TemplateView
from django.views.generic.edit import FormView
from django.urls import reverse_lazy

from accounts.models import Profile

from administration.models import AdminScheduledConsultation

import datetime
from personalityTest.models import Result
from psytests.forms import ContactForm

from django.core.mail import send_mail
from django.conf import settings

from riasec.models import Riasec_result

now = datetime.datetime.today()


class Notif:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context["unapproved_users"] = (
                Profile.objects.filter(is_assigned=False)
                .exclude(user__username=self.request.user or None)
                .count()
            )
            notif_count = (
                AdminScheduledConsultation.objects.filter(
                    managed_by__user=self.request.user or None,
                    is_done=False,
                    scheduled_date__date=now.date(),
                    scheduled_date__time__gt=now.time(),
                    user__is_assigned=True,
                ).count()
                + AdminScheduledConsultation.objects.filter(
                    managed_by__user=self.request.user or None,
                    is_done=False,
                    scheduled_date__lt=now.today(),
                    user__is_assigned=True,
                ).count()
            )
            context["notif_count"] = notif_count if notif_count is not None else None

        return context


class HomePageView(Notif, TemplateView):
    template_name = "homepage.html"



class Assessment(Notif, LoginRequiredMixin, FormView):
    template_name = "assessment.html"
    form_class = ContactForm
    success_url = reverse_lazy("homepage")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        obj = get_object_or_404(Profile, user__username = self.request.user)
        context['obj'] = obj
        
        try:
            context["personalityTest_results"] = Result.objects.get(
                user=self.request.user
            )
        except ObjectDoesNotExist:
            pass

        try:
            context["riasec_results"] = Riasec_result.objects.get(
                user=self.request.user
            )
        except ObjectDoesNotExist:
            pass

        return context


class Awesome(LoginRequiredMixin, TemplateView):
    template_name = "awesome.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['riasec'] = Riasec_result.objects.get(user__username=self.request.user)
        except ObjectDoesNotExist:
            pass

        try:
            context['personality'] = Result.objects.get(user__username=self.request.user)
        except ObjectDoesNotExist:
            pass
        return context
        
class DataPrivacyConsent(LoginRequiredMixin, TemplateView):
    template_name = 'privacy_consent.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        
        return context
