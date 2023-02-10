from django.http import JsonResponse
from django.views.generic import ListView
from django.shortcuts import redirect, render, HttpResponse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import user_passes_test
from .forms import AddIQQuestionForm, AddIQChoiceForm
from administration.views import Is_Counselor
from django.utils.html import strip_tags
from iqtest.models import Question, Choice
from django.core.paginator import Paginator

class IQView(LoginRequiredMixin, Is_Counselor, ListView):
    model = Question
    template_name = "iq/iq.html"
    context_object_name = "questions"
    paginate_by = 10
    ordering = ['id']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['add_question_form'] = AddIQQuestionForm()
        return context

class GetQuestions(IQView):
    template_name = "personality/questions.html"

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

@user_passes_test(lambda u:u.groups.filter(name="Counselor").exists())
def add_question(request):
    context = {}
    form = AddIQQuestionForm(request.POST or None)
    if form.is_valid():
        question = form.save()
        context['add_question_form'] = AddIQQuestionForm()
        questions = Question.objects.all().order_by('id')
        paginator = Paginator(questions, 10)  # 5 items per page
        page = request.GET.get('page')
        question_list = paginator.get_page(page)
        is_paginated = True if paginator.count > paginator.num_pages else False
        context['questions'] = question_list
        context['page_obj'] = question_list
        context['is_paginated'] = is_paginated
        context['changed'] = True
        messages.success(request, "Added Successfully", extra_tags="success")
        return render(request, 'iq/partials/add_question_field.html', context)
    if form.errors:
        context['add_question_form'] = form
        question_error = strip_tags(form.errors['question'])
        messages.warning(request, question_error, extra_tags="danger")
        return render(request, 'iq/partials/add_question_field.html', context)
    context['add_question_form'] = AddIQQuestionForm()
    return render(request, 'iq/partials/add_question_field.html', context)
@user_passes_test(lambda u:u.groups.filter(name="Counselor").exists())
def add_choice(request):
    context = {}
    form = AddIQChoiceForm(request.POST or None)
    if form.is_valid():
        instance = form.save()
        choices = Choice.objects.filter(question = instance.question)
        context['count'] = f"{choices.count() + 1}.)"
        context['choices'] = choices
    else:
        print(form.errors)
    return render(request, 'iq/partials/add_choice.html', context)
        

def delete_choice(request, id, question_id):
    context= {}
    question = Question.objects.filter(id=question_id).first()
    choice = Choice.objects.get(question=question, id=id)
    choice.delete()
    choices = Choice.objects.filter(question = question)
    context['count'] = f"{choices.count() + 1}.)"
    context['choices'] = choices
    return render(request, 'iq/partials/add_choice.html', context)

@user_passes_test(lambda u:u.groups.filter(name="Counselor").exists())
def delete_question(request):
    context = {}
    checkedboxes = request.POST.getlist('checked')

    if checkedboxes:
        Question.objects.filter(id__in=checkedboxes).delete()
        messages.success(request, 'Deleted Successfully' , extra_tags='success')
    else:
        data = messages.success(request, 'Please select a question to delete' , extra_tags='danger')

    questions = Question.objects.all().order_by('id')
    paginator = Paginator(questions, 10)  # 5 items per page
    page = request.GET.get('page')
    question_list = paginator.get_page(page)
    is_paginated = True if paginator.count > paginator.num_pages else False
    context['deleted'] = True
    context['questions'] = question_list
    context['page_obj'] = question_list
    context['is_paginated'] = is_paginated

    return render(request, 'iq/questions.html', context)


@user_passes_test(lambda u:u.groups.filter(name="Counselor").exists())
def update_question_form(request):
    context = {}
    if request.method == 'POST':
        questionid = request.POST["questionid"]
        question = Question.objects.get(id=questionid)
        form = AddIQQuestionForm(request.POST, instance = question)
        if form.is_valid():
            instance = form.save()
            questions = Question.objects.all().order_by('id')
            paginator = Paginator(questions, 10)  # 5 items per page
            page = request.GET.get('page')
            question_list = paginator.get_page(page)
            is_paginated = True if paginator.count > paginator.num_pages else False
            context['questions'] = question_list
            context['page_obj'] = question_list
            context['is_paginated'] = is_paginated
            context['question'] = instance
            context['changed'] = True
            return render(request, 'iq/partials/edit_question.html',context)
    question = Question.objects.get(id=request.GET['questionid'])
    form = AddIQQuestionForm(instance = question)
    context['question_to_update'] = question
    context["edit_mode"] = True
    context["edit_question_form"] = form
    return render(request, 'iq/partials/edit_question.html',context)

@user_passes_test(lambda u:u.groups.filter(name="Counselor").exists())
def update_question_view(request):
    context = {}
    question = Question.objects.get(id = request.GET['questionid'])
    context['question'] = question
    context['update_choice_form'] = AddIQChoiceForm(initial={
        "question": question
    })
    choices = Choice.objects.filter(question = question)
    context['count'] = f"{choices.count() + 1}.)"
    context['choices'] = choices
    return render(request, 'iq/partials/update_question.html', context)

