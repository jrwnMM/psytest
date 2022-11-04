from django.http import JsonResponse
from django.views.generic import ListView
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import user_passes_test

from .forms import AddPQuestionsForm
from administration.views import Is_Counselor

from personalityTest.models import Question

class PersonalityView(LoginRequiredMixin, Is_Counselor, ListView):
    model = Question
    template_name = "personality/personality.html"
    context_object_name = "questions"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['add_form'] = AddPQuestionsForm()
        return context

class GetQuestions(PersonalityView):
    template_name = "personality/questions.html"

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

@user_passes_test(lambda u:u.groups.filter(name="Counselor").exists())
def add_question(request):
    form = AddPQuestionsForm(request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, 'Created successfully', extra_tags="success")
        return redirect('administration:get-personality-questions')
    else:
        messages.warning(request, 'Error', extra_tags="danger")
        return redirect('administration:get-personality-questions')

@user_passes_test(lambda u:u.groups.filter(name="Counselor").exists())
def update_question(request, pk):
    question = Question.objects.get(id=pk)
    form = AddPQuestionsForm(request.POST or None, instance=question)
    context = {}

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Updated successfully', extra_tags="success")
            return redirect('administration:get-personality-questions')
        else:   
            messages.warning(request, 'Error', extra_tags="danger")
            return redirect('administration:update-personality-question', pk=pk)

    context['form'] = form
    return render(request, "personality/partials/form.html", context)

@user_passes_test(lambda u:u.groups.filter(name="Counselor").exists())
def delete_question(request):
    if request.is_ajax:
        checkedboxes = request.GET.getlist('checkedboxes[]')
        if checkedboxes:
            Question.objects.filter(id__in=checkedboxes).delete()
            data = messages.success(request, 'Deleted Successfully' , extra_tags='success')
        else:
            data = messages.success(request, 'Please select a question to delete' , extra_tags='danger')

    return JsonResponse(data, safe=False)
    
