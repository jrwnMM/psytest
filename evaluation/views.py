from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import EssayQuestion, RatingQuestion, UserFeedback

# Create your views here.

class EvaluationView(LoginRequiredMixin, TemplateView):
    template_name = "evaluation/view.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["ratings"] = RatingQuestion.objects.all()
        context["essays"] = EssayQuestion.objects.all()

        return context

    def post(self, request, *args, **kwargs):
        user = self.request.user
        ratings = RatingQuestion.objects.all()
        essays = EssayQuestion.objects.all()
        rate_answers = []
        essay_answers = []
        for rating in ratings.iterator():
            value = int(self.request.POST[f"rate_{rating.id}"])
            rate_answers.append(value)

        for essay in essays.iterator():
            answer = self.request.POST[f"essay_{essay.id}"]
            essay_answers.append(answer)

        print("PRINT", essay_answers)
        obj = UserFeedback.objects.create(
            user=user,
            q_1=rate_answers[0],
            q_2=rate_answers[1],
            q_3=rate_answers[2],
            q_4=rate_answers[3],
            q_5=rate_answers[4],
            q_6=rate_answers[5],
            q_7=rate_answers[6],
            q_8=rate_answers[7],
            e_1=essay_answers[0],
            e_2=essay_answers[1],
            e_3=essay_answers[2],
            e_4=essay_answers[3],
        )
        obj.save()

        return redirect('assessment')
