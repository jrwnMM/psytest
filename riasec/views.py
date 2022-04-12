from django.shortcuts import redirect, render
from django.views.generic.base import TemplateView
from accounts.models import Profile

from personalityTest.models import Result
from .models import RIASEC_Test, Riasec_result
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages

from datetime import datetime
from django.utils import timezone
# Create your views here.


@login_required(login_url="accounts:login")
def testPage(request):
    range_num = range(42)
    obj = Riasec_result.objects.all()
    questions = RIASEC_Test.objects.all()

    if (request.user.profile.department):
        return render(
            request,
            "riasec/test.html",
            {"questions": questions, "obj": obj, "range": range_num},
        )
    else:
        messages.error(request, 'Please enter Department,Program and Year')
        return redirect('accounts:edit_user')



@login_required(login_url="accounts:login")
def evaluate(request):
    now = datetime.now()
    name = request.user
    r = []
    i = []
    a = []
    s = []
    e = []
    c = []

    for id in range(1, 43):
        score = float(request.POST.get(f"{id}"))
        question = RIASEC_Test.objects.get(pk=id)

        if question.category == "R":
            r.append(score)
        if question.category == "I":
            i.append(score)
        if question.category == "A":
            a.append(score)
        if question.category == "S":
            s.append(score)
        if question.category == "E":
            e.append(score)
        if question.category == "C":
            c.append(score)

    r = (sum(r) / 7) * 100
    i = (sum(i) / 7) * 100
    a = (sum(a) / 7) * 100
    s = (sum(s) / 7) * 100
    e = (sum(e) / 7) * 100
    c = (sum(c) / 7) * 100
    


    try:
        obj = Riasec_result.objects.get(user=request.user)
        obj.user=request.user
        obj.realistic=r
        obj.investigative=i
        obj.artistic=a
        obj.social=s
        obj.enterprising=e
        obj.conventional=c
        obj.save()

    except ObjectDoesNotExist:
        result = Riasec_result.objects.create(
            user=request.user,
            realistic=r,
            investigative=i,
            artistic=a,
            social=s,
            enterprising=e,
            conventional=c,
        )
        result.save()

    try:
        obj = Result.objects.get(user__username=name)
        obj2 = Riasec_result.objects.get(user__username=name)

        if obj and obj2:
            obj3 = Profile.objects.get(user__username=name)
            obj3.is_assigned = False
            obj3.test_completed = now
            obj3.save()
    except ObjectDoesNotExist:
            pass

    return redirect('awesome')






