from django.shortcuts import redirect, render, HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.db import transaction
from django.db.models import Q

from accounts.models import Profile
from riasec.models import Question, Result as RResult, Answer
from personalityTest.models import Result as PResult

from datetime import datetime
# Create your views here.


@login_required(login_url="accounts:login")
def testPage(request):
    if not len(Question.objects.filter(category__in=["R", "I", "A", "S", "E", "C"]).order_by("category").distinct("category")) == 6:
        return HttpResponse("Not available")
    if (request.user.profile.department):
        return render(request,"riasec/test.html")
    else:
        messages.error(request, 'Please enter Department,Program and Year')
        return redirect('accounts:edit_user')

def test_container(request):
    questions = Question.objects.all()
    return render(
            request,
            "riasec/partials/test_container.html",
            {"questions": questions},
        )

@transaction.atomic
@login_required(login_url="accounts:login")
def evaluate(request):
    now = datetime.now()
    user = request.user
    q = Question.objects.all().order_by('pk').values_list('id', flat=True)
    
    r = []
    i = []
    a = []
    s = []
    e = []
    c = []

    for id in q.iterator():
        question = Question.objects.get(pk=id)
        score = None if request.POST.get(f"{id}") == None else float(request.POST.get(f"{id}"))

        answer = Answer()
        answer.question = question
        answer.answer = score
        answer.user = user
        answer.save()
        
        if score:
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

    r = 0 if len(r) == 0 else (sum(r) / len(r)) * 100
    i = 0 if len(i) == 0 else (sum(i) / len(i)) * 100
    a = 0 if len(a) == 0 else(sum(a) / len(a)) * 100
    s = 0 if len(s) == 0 else(sum(s) / len(s)) * 100
    e = 0 if len(e) == 0 else(sum(e) / len(e)) * 100
    c = 0 if len(c) == 0 else(sum(c) / len(c)) * 100

    result = RResult.objects.create(
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
        obj3 = Profile.objects.get(user__username=user)
        obj3.last_test_taken = now
        obj3.save()
    except ObjectDoesNotExist:
            pass

    return redirect('awesome', test='careertest')






