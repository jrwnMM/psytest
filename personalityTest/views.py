from django.shortcuts import redirect, HttpResponse
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
import joblib
import pandas as pd
from accounts.models import Profile
from personalityTest.models import (
    Question,
    RecommendedProgram,
    Result as PResult,
    Answer,
)
from riasec.models import OfferedProgram
from datetime import datetime


class TestView(LoginRequiredMixin, TemplateView):
    template_name = "personalityTest/testPage.html"
    ml_model = joblib.load("models/personality_career_dt.sav")

    def get(self, *args, **kwargs):
        if (
            not len(
                Question.objects.filter(
                    category__in=["EXT", "EST", "AGR", "CSN", "OPN"]
                )
                .order_by("category")
                .distinct("category")
            )
            == 5
        ):
            return HttpResponse("Not available")
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["questions"] = Question.objects.all()

        try:
            context["existed"] = PResult.objects.get(user=self.request.user)
        except ObjectDoesNotExist:
            pass

        return context

    @transaction.atomic
    def post(self, *args, **kwargs):
        now = datetime.now()
        user = self.request.user
        q = Question.objects.all().order_by("pk").values_list("id", flat=True)
        ext = []
        est = []
        agr = []
        csn = []
        opn = []

        for id in q.iterator():
            score = float(self.request.POST.get(f"{id}"))
            question = Question.objects.get(pk=id)

            if question.key == "0":
                if score == 5:
                    score = 1
                if score == 4:
                    score = 2

            try:
                answer = Answer.objects.get(user=self.request.user, question=question)
                answer.answer = score
                answer.save()
            except Answer.DoesNotExist:
                answer = Answer()
                answer.question = question
                answer.answer = score
                answer.user = user
                answer.save()
            if question.category == "EXT":
                ext.append(score)
            if question.category == "EST":
                est.append(score)
            if question.category == "AGR":
                agr.append(score)
            if question.category == "CSN":
                csn.append(score)
            if question.category == "OPN":
                opn.append(score)

        extroversion = float(sum(ext)) / len(ext)
        neurotic = float(sum(est))/ len(est)
        agreeable = float(sum(agr)) / len(agr)
        conscientious = float(sum(csn)) / len(csn)
        openness = float(sum(opn)) / len(opn)

        # career_prediction = model.predict
        personality = [[extroversion, neurotic, agreeable, conscientious, openness]]

        program_prediction = self.program_predictor(personality)
        first_ranked = self.first_ranked(program_prediction)

        programs = []
        for key, value in first_ranked.items():
            try:
                offeredPrograms = OfferedProgram.objects.filter(interest=key)
                if offeredPrograms:
                    for item in offeredPrograms:
                        programs.append(item)
            except ObjectDoesNotExist:
                pass

        if programs:
            if RecommendedProgram.objects.filter(user=user).exists():
                RecommendedProgram.objects.filter(user=user).delete()

            for obj in set(programs):
                recCareer = RecommendedProgram()
                recCareer.user = user
                recCareer.offeredProgram = obj
                recCareer.save()

        try:
            obj = PResult.objects.get(user=user)
            obj.user = user
            obj.extroversion = extroversion
            obj.neurotic = neurotic
            obj.agreeable = agreeable
            obj.conscientious = conscientious
            obj.openness = openness
            obj.save()

        except ObjectDoesNotExist:
            result = PResult.objects.create(
                user=user,
                extroversion=extroversion,
                neurotic=neurotic,
                agreeable=agreeable,
                conscientious=conscientious,
                openness=openness,
            )
            result.save()

        try:
            obj3 = Profile.objects.get(user__username=user)
            obj3.last_test_taken = now
            obj3.save()
        except ObjectDoesNotExist:
            pass

        return redirect("awesome", test='personalitytest')

    def program_predictor(self, personality):
        prediction = self.ml_model.predict(personality)
        return prediction

    def first_ranked(self, prediction):
        first = {}

        obj = {
            "realistic": prediction[0][0],
            "investigative": prediction[0][1],
            "artistic": prediction[0][2],
            "social": prediction[0][3],
            "enterprising": prediction[0][4],
            "conventional": prediction[0][5],
        }

        sorted_obj = {
            key: value
            for key, value in sorted(
                obj.items(), key=lambda item: item[1], reverse=True
            )
        }

        for key, value in sorted_obj.items():
            if list(sorted_obj.values())[0] == value:
                first[key] = value

        return first
