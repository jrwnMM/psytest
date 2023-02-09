from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic import TemplateView
from django.db import transaction
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin,
)
from .forms import UpdateProfileForm

from accounts.models import Profile
from riasec.models import OfferedProgram, Result as CareerResult
from personalityTest.models import RecommendedProgram, Result as PersonalityResult
from iqtest.models import Result as IQResult

from psytests.forms import ContactForm


from django.contrib.auth import get_user_model
User = get_user_model()

class UserDetailViewMixin(UserPassesTestMixin):
    def test_func(self):
        test = True
        obj = get_object_or_404(Profile, user=self.request.user)
        if obj.user.is_superuser:
            test = True
        else:
            if obj.user.username != self.kwargs["username"]:
                test = False
        return test

class UserStats(LoginRequiredMixin, UserDetailViewMixin, TemplateView):
    template_name = "userprofile/stats.html"

    def get_context_data(self, **kwargs):
        context = super(UserStats, self).get_context_data(**kwargs)
        context['form'] = ContactForm()
        obj = Profile.objects.get(user__username=self.kwargs.get("username"))
        context["profile"] = obj

        try:
            context["riasec_result"] = CareerResult.objects.get(user__id=self.kwargs.get("pk")
)
            obj = (
                CareerResult.objects.filter(
                    user__username=self.kwargs.get("username"),
                )
                .values("realistic","investigative","artistic","social","enterprising","conventional",)
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
        except CareerResult.DoesNotExist:
            pass
        
        try:
            context["personalityTest_result"] = PersonalityResult.objects.get(user__id=self.kwargs.get("pk"))
        except PersonalityResult.DoesNotExist:
            pass
        iq_result = IQResult.objects.filter(user__id = self.kwargs.get("pk")).first()
        context['iq_result'] = iq_result

        if iq_result:
            if iq_result.result in range(36,41):
                result_desc = 'Exceptional'
            if iq_result.result in range(25,31):
                result_desc = 'Very Good'
            if iq_result.result in range(19,25):
                result_desc = 'Good'
            if iq_result.result in range(15,19):
                result_desc = 'Average'
            if iq_result.result in range(0,15):
                result_desc = 'Poor'
        context['iqresult_desc'] = result_desc
        context['recommended_programs'] = RecommendedProgram.objects.filter(user__username=self.kwargs.get("username"))
        context['realistic_programs'] = OfferedProgram.objects.filter(interest='realistic')
        context['investigative_programs'] = OfferedProgram.objects.filter(interest='investigative')
        context['artistic_programs'] = OfferedProgram.objects.filter(interest='artistic')
        context['social_programs'] = OfferedProgram.objects.filter(interest='social')
        context['enterprising_programs'] = OfferedProgram.objects.filter(interest='enterprising')
        context['conventional_programs'] = OfferedProgram.objects.filter(interest='conventional')
        
        return context

class EditProfile(LoginRequiredMixin, TemplateView):
    template_name = 'userprofile/profile-edit.html'

    def get_context_data(self, **kwargs):
        profile = Profile.objects.get(user__username=self.kwargs['username'])
        context = super(EditProfile, self).get_context_data(**kwargs)
        context['profile_form'] = UpdateProfileForm(instance=profile, initial={
            'first_name': profile.user.first_name,
            'last_name': profile.user.last_name,
            'educationlevel': profile.educationlevel,
            'department': profile.department,
            'program': profile.program,
            'year': profile.year,
        })
        context['profile'] = profile
        return context
            
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        user_profile = Profile.objects.get(user__username=self.kwargs['username'])
        form = UpdateProfileForm(self.request.POST, instance=user_profile)
        context = self.get_context_data()

        if form.is_valid():
            profile = form.save(commit=False)
            profile.user.first_name = form.cleaned_data.get('first_name')
            profile.user.last_name = form.cleaned_data.get('last_name')
            profile.save()
            profile.user.save()
            return redirect(reverse('profile:user-stats', kwargs={"username":self.kwargs['username'], "pk":self.kwargs['pk'], "tab":"profile"}))
        else:
            context['profile_form_errors'] = form.errors
            return render(self.request, self.template_name, context)

def departments(request, username, pk):
    form=UpdateProfileForm(request.GET)
    return HttpResponse(form['department'])

def programs(request, username, pk):
    form=UpdateProfileForm(request.GET)
    return HttpResponse(form['program'] or '')

def years(request, username, pk):
    form = UpdateProfileForm(request.GET)
    response = HttpResponse(form['year'] or None)
    return response