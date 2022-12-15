from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render, HttpResponse
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from accounts.models import Department, Program
from administration.organization.forms import AddDepartmentForm, AddProgramForm
from administration.views import Is_Counselor
from accounts.models import EducationLevel, Department, Year
from django_htmx.http import trigger_client_event

class DepartmentListView(LoginRequiredMixin, Is_Counselor, ListView):
    template_name = 'organization/department/list.html'
    paginate_by = 10
    context_object_name = 'departments'
    
    def get_queryset(self):
        return Department.objects.all().order_by('name')

    def get_context_data(self, **kwargs):
        context = super(DepartmentListView, self).get_context_data(**kwargs)
        context['form'] = AddDepartmentForm()
        context['edu_levels'] = EducationLevel.objects.all()
        context['departments'] = Department.objects.all()
        context['years'] = Year.objects.all()
        return context

def edu_level_options(request):
    context = {}
    context["edu_levels"] = EducationLevel.objects.all()
    return render(request, 'organization/partials/education_level_options.html', context)

def add_education_level(request):
    edu_text = request.POST['edu_text']
    edu_level, created = EducationLevel.objects.get_or_create(name=edu_text)
    context = {}
    if created:
        context["edu_levels"] = EducationLevel.objects.all()
        # response = render(request, 'organization/partials/education_levels.html', context)
        response = HttpResponse("<div class='text-success'>Added</div>")
        trigger_client_event(response, "edu_level_options", {})
        return response
    
    return HttpResponse("<div class='text-danger'>Already Existed</div>")

def delete_education_level(request):
    print(request)
    



@user_passes_test(lambda u:u.groups.filter(name="Counselor").exists())
def addDepartment(request):
    form = AddDepartmentForm(request.POST or None)
    data = {}
    if form.is_valid():
        form.save()
        data['message'] = messages.success(request, "%s department is added successfully" %form.cleaned_data['name'], extra_tags='success' )
        return JsonResponse(data, status=200)
    else:
        data['form'] = form.errors
        return JsonResponse(data, status=400)


class DepartmentDetailView(LoginRequiredMixin, Is_Counselor, DetailView):
    template_name = 'organization/department/details.html'
    context_object_name = 'department'

    def get_object(self):
        return get_object_or_404(Department, code=self.kwargs['code'])

    def get_context_data(self, **kwargs):
        context = super(DepartmentDetailView, self).get_context_data(**kwargs)
        programs= self.get_department_programs()
        context['form'] = AddProgramForm(initial={'department': self.get_object()})
        context['department_programs'] = programs
        context['is_paginated'] = programs.has_other_pages
        context['page_obj'] = programs
        return context
    
    def get_department_programs(self):
        queryset = self.object.programs.all().order_by('name') 
        paginator = Paginator(queryset, 5) #paginate_by
        page = self.request.GET.get('page')
        programs = paginator.get_page(page)
        return programs
        
@user_passes_test(lambda u:u.groups.filter(name="Counselor").exists())
def addProgram(request):
    form = AddProgramForm(request.POST or None)
    data = {}
    if form.is_valid():
        form.save()
        data['message'] = messages.success(request, "%s program is added successfully" %form.cleaned_data['name'], extra_tags='success' )
        return JsonResponse(data, status=200)
    else:
        data['form'] = form.errors
        return JsonResponse(data, status=400)

@user_passes_test(lambda u:u.groups.filter(name="Counselor").exists())
def deleteProgram(request, id):
    try:
        program = Program.objects.get(pk=id)
        program.delete()
        messages.info(request, f'{program.name} is deleted successfully', extra_tags='info')
    except Program.DoesNotExist:
        messages.warning(request, 'Program does not exist', extra_tags='danger')

    return redirect('administration:department-details', code=program.department.code)

@user_passes_test(lambda u:u.groups.filter(name="Counselor").exists())
def delete_department(request):
    if request.is_ajax:
        checkedboxes = request.GET.getlist('checkedboxes[]')
        if checkedboxes:
            Department.objects.filter(id__in=checkedboxes).delete()
            data = messages.success(request, 'Deleted Successfully' , extra_tags='success')
        else:
            data = messages.success(request, 'Please select a department to delete' , extra_tags='danger')

    return JsonResponse(data, safe=False)

@user_passes_test(lambda u:u.groups.filter(name="Counselor").exists())
def delete_program(request):
    if request.is_ajax:
        checkedboxes = request.GET.getlist('checkedboxes[]')
        if checkedboxes:
            Program.objects.filter(id__in=checkedboxes).delete()
            data = messages.success(request, 'Deleted Successfully' , extra_tags='success')
        else:
            data = messages.success(request, 'Please select a program to delete' , extra_tags='danger')

    return JsonResponse(data, safe=False)