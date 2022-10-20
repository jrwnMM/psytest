from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404, redirect
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.urls import reverse_lazy, reverse
from accounts.models import Profile
from django.contrib import messages
from django.shortcuts import render

from personalityTest.models import Result as PResult
from psytests.forms import ContactForm

from riasec.models import Result as RResult


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

        try:
            context["personality_result"] = PResult.objects.get(
                user=self.request.user
            )
        except ObjectDoesNotExist:
            pass

        try:
            context["career_result"] = RResult.objects.get(user=self.request.user)
        except ObjectDoesNotExist:
            pass

        return context


class Awesome(LoginRequiredMixin, TemplateView):
    template_name = "awesome.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context["riasec"] = RResult.objects.get(user=self.request.user)
        except ObjectDoesNotExist:
            pass

        try:
            context["personality"] = PResult.objects.get(user=self.request.user)
        except ObjectDoesNotExist:
            pass
        return context


class DataPrivacyConsent(LoginRequiredMixin, TemplateView):
    template_name = "privacy_consent.html"

    def get(self, request, *args, **kwargs):
        user = self.request.user
        is_gradeSchool = user.profile.educationlevel.name == "Grade School" and ((user.profile.department and user.profile.year) is None)
        is_userdetails_complete = user.profile.educationlevel.name != "Grade School" and (user.profile.department and user.profile.program and user.profile.year) is None
        
        print(is_userdetails_complete)

        if is_gradeSchool or is_userdetails_complete:
            messages.info(request, "Please complete your educational background", extra_tags="info")
            return redirect(reverse("profile:edit-profile", kwargs={"username": user.username, "pk": user.id}))

        return render(request, self.template_name, {"test": self.kwargs["test"]})
