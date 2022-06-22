from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404, redirect
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.urls import reverse_lazy, reverse
from accounts.models import Profile
from django.contrib import messages
from django.shortcuts import render
from django_htmx.http import trigger_client_event

from personalityTest.models import Result as PResult
from psytests.forms import ContactForm

from django.conf import settings

from riasec.models import Result as RResult



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
        context['request_status'] = obj.is_assigned
        
        try:
            context["personalityTest_results"] = PResult.objects.get(user=self.request.user)
        except ObjectDoesNotExist:
            pass

        try:
            context["riasec_results"] = RResult.objects.get(user=self.request.user)
        except ObjectDoesNotExist:
            pass

        return context


class Awesome(LoginRequiredMixin, TemplateView):
    template_name = "awesome.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['riasec'] = RResult.objects.get(user=self.request.user)
        except ObjectDoesNotExist:
            pass

        try:
            context['personality'] = PResult.objects.get(user=self.request.user)
        except ObjectDoesNotExist:
            pass
        return context
        
class DataPrivacyConsent(LoginRequiredMixin, TemplateView):
    template_name = 'privacy_consent.html'

    def get(self, request, *args, **kwargs):
        user = self.request.user
        if (user.profile.department and user.profile.program and user.profile.year):
            return render(request, self.template_name, {
                'test': self.kwargs['test']
            })
        else:
            messages.info(request, 'Please complete your educational background', extra_tags="info")
            return redirect(reverse('profile:edit-profile', kwargs={'username':user.username, 'pk':user.id}))

def request_counsel(request):
    context = {}
    profile = Profile.objects.get(id=request.user.id)

    if profile.is_assigned is False:
        profile.is_assigned = None
        messages.success(request, 'Request canceled', extra_tags="success")
        profile.save()
    elif profile.is_assigned is None:
        profile.is_assigned = False
        messages.success(request, 'Request Sent', extra_tags="success")
        profile.save()

    context['request_status'] = profile.is_assigned

    response = render(request, 'partials/request-section.html', context)
    trigger_client_event(response, 'confirm_request', {})
    trigger_client_event(response, 'alert', {})
    return  response