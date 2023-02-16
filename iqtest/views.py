from django.shortcuts import redirect, HttpResponse
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.models import Profile

from .models import Question, Answer, Choice, Result

# Create your views here.


class TestView(LoginRequiredMixin, TemplateView):
    template_name = "iqtest/testPage.html"

    def get(self, request, *args, **kwargs):
        iq_questionnaires = Question.objects.all().count()
        if  not iq_questionnaires < 40:
            return HttpResponse("Not Available")
        return super().get(request, *args, **kwargs)


class TestContainer(LoginRequiredMixin, TemplateView):
    template_name = "iqtest/partials/test_container.html"

    def post(self, request):
        user = Profile.objects.get(user=request.user)
        totalscore = 0
        for i in request.POST:
            if i != "csrfmiddlewaretoken":
                splitted = request.POST[i].split(":")
                if splitted[1] == "correct":
                    totalscore += 1
        result = Result.objects.create(user=user, result = totalscore)
        for i in request.POST:
            if i != "csrfmiddlewaretoken":
                question = Question.objects.get(id=i)
                splitted = request.POST[i].split(":")
                choice = Choice.objects.get(id=splitted[0])
                answer = Answer()
                answer.question = question
                answer.answer = choice
                answer.user = user
                answer.result = result
                answer.save()
        return redirect('awesome', test='iqtest')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["questions"] = Question.objects.all().order_by("id")
        context["started"] = True
        questions = Question.objects.all()
        return context

