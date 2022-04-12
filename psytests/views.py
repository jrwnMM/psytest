from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.urls import reverse_lazy

from accounts.models import Profile


import datetime
from personalityTest.models import Result
from psytests.forms import ContactForm

from django.conf import settings

from riasec.models import Riasec_result



class HomePageView(TemplateView):
    template_name = "homepage.html"



class Assessment(LoginRequiredMixin, FormView):
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
