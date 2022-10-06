import csv
from django.shortcuts import render, HttpResponse

from generalIQ.models import Question

# Create your views here.
def generalIQTest(request):
    context = {}
    questions = Question.objects.all()
    context["questions"] = questions
    return render(request, "generalIQ/generaliqtest.html", context)