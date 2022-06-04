from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.db import transaction

from accounts.models import Profile
from riasec.models import Question, Result as RResult, Answer
from personalityTest.models import Result as PResult

from datetime import datetime
# Create your views here.


@login_required(login_url="accounts:login")
def testPage(request):
    range_num = range(42)
    obj = RResult.objects.all()
    questions = Question.objects.all()

    if (request.user.profile.department):
        return render(
            request,
            "riasec/test.html",
            {"questions": questions, "obj": obj, "range": range_num},
        )
    else:
        messages.error(request, 'Please enter Department,Program and Year')
        return redirect('accounts:edit_user')


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
        score = float(request.POST.get(f"{id}"))
        question = Question.objects.get(pk=id)
        print(id)

        
        try:
            answer = Answer.objects.get(user=user, question=question)
            answer.answer = score
            answer.save()
        except Answer.DoesNotExist:
            answer = Answer()
            answer.question = question
            answer.answer = score
            answer.user = user
            answer.save()

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

    r = (sum(r) / len(r)) * 100
    i = (sum(i) / len(i)) * 100
    a = (sum(a) / len(a)) * 100
    s = (sum(s) / len(s)) * 100
    e = (sum(e) / len(e)) * 100
    c = (sum(c) / len(c)) * 100
    


    try:
        obj = RResult.objects.get(user=request.user)
        obj.user=request.user
        obj.realistic=r
        obj.investigative=i
        obj.artistic=a
        obj.social=s
        obj.enterprising=e
        obj.conventional=c
        obj.save()

    except ObjectDoesNotExist:
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

    return redirect('awesome')






