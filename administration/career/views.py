from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import user_passes_test
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.generic import ListView
from django.contrib import messages
from administration.views import SuperUserCheck

from .forms import AddCareerQuestionForm

from riasec.models import Question

class CareerView(LoginRequiredMixin, SuperUserCheck, ListView):
    model = Question
    template_name = "career/career.html"
    context_object_name = "questions"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['add_form'] = AddCareerQuestionForm()
        return context



class GetQuestions(CareerView):
    template_name = "career/questions.html"

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

@user_passes_test(lambda u: u.is_superuser)
def add_question(request):
    form = AddCareerQuestionForm(request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, 'Created successfully', extra_tags="success")
        return redirect('administration:get-career-questions')
    else:
        messages.warning(request, 'Error', extra_tags="danger")
        return redirect('administration:get-career-questions')

@user_passes_test(lambda u: u.is_superuser)
def update_question(request, pk):
    question = Question.objects.get(id=pk)
    form = AddCareerQuestionForm(request.POST or None, instance=question)
    context = {}

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Updated successfully', extra_tags="success")
            return redirect('administration:get-career-questions')
        else:   
            messages.warning(request, 'Error', extra_tags="danger")
            return redirect('administration:update-career-question', pk=pk)

    context['form'] = form
    return render(request, "career/partials/form.html", context)

@user_passes_test(lambda u: u.is_superuser)
def delete_question(request):
    if request.is_ajax:
        checkedboxes = request.GET.getlist('checkedboxes[]')
        if checkedboxes:
            Question.objects.filter(id__in=checkedboxes).delete()
            data = messages.success(request, 'Deleted Successfully' , extra_tags='success')
        else:
            data = messages.success(request, 'Please select a question to delete' , extra_tags='danger')

    return JsonResponse(data, safe=False)
    