from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from django.views.generic.base import TemplateView
from accounts.models import Profile

from personalityTest.models import Result
from .models import RIASEC_Test, Riasec_result
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView
from django.views.generic.edit import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages


# Create your views here.


@login_required(login_url="accounts:login")
def testPage(request):
    range_num = range(42)
    obj = Riasec_result.objects.all()
    questions = RIASEC_Test.objects.all()
    return render(
        request,
        "riasec/test.html",
        {"questions": questions, "obj": obj, "range": range_num},
    )

@login_required(login_url="accounts:login")
def evaluate(request):
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
            obj3.save()
    except ObjectDoesNotExist:
            pass

    return redirect('awesome')


class Home(LoginRequiredMixin, ListView):
    model = Riasec_result
    template_name = "riasec/riasec_home.html"
    context_object_name = "result"

    def get_queryset(self):
        try:
            result = Riasec_result.objects.get(user=self.request.user)
        except ObjectDoesNotExist:
            result = None
        return result

class ResultPage(LoginRequiredMixin, TemplateView):
    template_name = "riasec/resultPage.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            result = Riasec_result.objects.get(user=self.request.user)
            context['result'] = result
        except ObjectDoesNotExist:
            None

        
        try:
            obj = Riasec_result.objects.filter(user=self.request.user).values(
            "realistic",
            "investigative",
            "artistic",
            "social",
            "enterprising",
            "conventional",
            ).first()
            if obj is not None:
                objects = dict(sorted(obj.items(), key=lambda item: item[1], reverse=True))
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

        return context


