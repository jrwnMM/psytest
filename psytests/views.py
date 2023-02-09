from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.urls import reverse, reverse_lazy
from accounts.models import Profile
from django.contrib import messages
from django.shortcuts import render
from django.db.models import Q
from personalityTest.models import Result as PResult
from riasec.models import Result as RResult
from iqtest.models import Result as IQResult
from psytests.forms import ContactForm



class HomePageView(TemplateView):
    template_name = "homepage.html"


class Assessment(LoginRequiredMixin, FormView):
    template_name = "assessment.html"
    form_class = ContactForm
    success_url = reverse_lazy("homepage")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = get_object_or_404(Profile, user__username=self.request.user)
        context["profile"] = obj
        context["personality_result"] = PResult.objects.filter(user=self.request.user).last()
        context["career_result"] = RResult.objects.filter(user=self.request.user).last()
        context["iq_result"]= IQResult.objects.filter(user=self.request.user.profile).last()
        return context


class Awesome(LoginRequiredMixin, TemplateView):
    template_name = "awesome.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        if kwargs['test'] == 'iqtest':
            context['typeOfTest'] = "IQ test"
        if kwargs['test'] == 'personalitytest':
            context['typeOfTest'] = "personality test"
        if kwargs['test'] == 'careertest':
            context['typeOfTest'] = "career test"
        context["riasec"] = RResult.objects.filter(user=self.request.user).last()
        context["personality"]= PResult.objects.filter(user=self.request.user).last()
        context["iq"]= IQResult.objects.filter(user=self.request.user.profile).last()
        return context


class DataPrivacyConsent(LoginRequiredMixin, TemplateView):
    template_name = "privacy_consent.html"

    def get(self, request, *args, **kwargs):
        user = self.request.user
        userprofile = user.profile
        if not Profile.objects.filter(
            Q(user=user)
            & Q(educationlevel__isnull=False)
            & Q(department__isnull=False)
            & Q(year__isnull=False)
        ).exists():

            messages.info(
                request,
                "Please complete your educational background",
                extra_tags="info",
            )
            return redirect(
                reverse(
                    "profile:edit-profile",
                    kwargs={"username": user.username, "pk": user.id},
                )
            )
        else:
            return render(request, self.template_name, {"test": self.kwargs["test"]})
            # return render(request, "testnotrdy.html")

