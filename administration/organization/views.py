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


class OrganizationView(LoginRequiredMixin, Is_Counselor, ListView):
    template_name = "organization/list.html"

    def get_queryset(self):
        return Department.objects.all().order_by("name")

    def get_context_data(self, **kwargs):
        context = super(OrganizationView, self).get_context_data(**kwargs)
        context["form"] = AddDepartmentForm()
        context["edu_levels"] = EducationLevel.objects.all()
        context["departments"] = Department.objects.all()
        context["years"] = Year.objects.all()
        return context


@user_passes_test(lambda u: u.groups.filter(name="Counselor").exists())
def edu_level_options(request):
    context = {}
    context["edu_levels"] = EducationLevel.objects.all()
    return render(
        request, "organization/partials/education_level_options.html", context
    )


@user_passes_test(lambda u: u.groups.filter(name="Counselor").exists())
def edu_levels_list_body(request):
    context = {}
    context["edu_levels"] = EducationLevel.objects.all()
    return render(request, "organization/partials/edu_levels_list_body.html", context)


@user_passes_test(lambda u: u.groups.filter(name="Counselor").exists())
def department_program_list(request, dept_id):
    context = {}
    dept = Department.objects.get(id=dept_id)
    context["programs"] = dept.programs.all()
    context["dept_code"] = dept.code
    return render(request, "organization/partials/dept_prog_list.html", context)


@user_passes_test(lambda u: u.groups.filter(name="Counselor").exists())
def add_education_level(request):
    edu_text = request.POST["edu_text"]
    edu_level, created = EducationLevel.objects.get_or_create(name=edu_text)
    context = {}
    if created:
        context["success"] = True
        context["edu_levels"] = EducationLevel.objects.all()
        response = render(
            request, "organization/partials/edu_levels_list_body.html", context
        )
        trigger_client_event(response, "update_edu_level_options", {})
        return response
    else:
        context["failed"] = True
    return render(request, "organization/partials/edu_levels_list_body.html", context)


@user_passes_test(lambda u: u.groups.filter(name="Counselor").exists())
def delete_education_level(request):
    context = {}
    checked = request.POST.getlist("edu_levels_id")
    EducationLevel.objects.filter(id__in=checked).delete()
    context["success"] = True
    context["edu_levels"] = edu_levels = EducationLevel.objects.all()
    response = render(
        request, "organization/partials/edu_levels_list_body.html", context
    )
    trigger_client_event(response, "update_edu_level_options", {})
    return response


@user_passes_test(lambda u: u.groups.filter(name="Counselor").exists())
def add_department(request):
    context = {}
    edu_level_id = request.POST["edu_level"]
    if not edu_level_id:
        context["missing"] = True
        return render(request, "organization/partials/department_list.html", context)
    try:
        department_name = request.POST["name"]
        department_code = request.POST["code"]
        if not Department.objects.filter(
            educationlevel__id=edu_level_id, code=department_code
        ).exists():
            education_level = EducationLevel.objects.get(id=edu_level_id)
            new_department = Department()
            new_department.educationlevel = education_level
            new_department.name = department_name
            new_department.code = department_code
            new_department.save()
            context["success"] = True
            context["yearlevels"] = Year.objects.filter(educationlevel=education_level)
        else:
            context["code_exists"] = True
    except EducationLevel.DoesNotExist:
        context["failed"] = True

    context["departments"] = Department.objects.filter(educationlevel__id=edu_level_id)
    return render(
        request, "organization/partials/department_list.html", context, status=200
    )


@user_passes_test(lambda u: u.groups.filter(name="Counselor").exists())
def add_department_program(request):
    context = {}
    dept_code = request.POST["department"]
    educationlevel = request.POST["educationlevel"]
    program_name = request.POST["program_name"]
    program_code = request.POST["program_code"]

    try:
        if not Program.objects.filter(
            department__code=dept_code, code=program_code
        ).exists():
            department = Department.objects.get(educationlevel__id=educationlevel, code=dept_code)
            new_dept_prog = Program()
            new_dept_prog.department = department
            new_dept_prog.name = program_name
            new_dept_prog.code = program_code
            new_dept_prog.save()
            context["success"] = True
        else:
            context["code_exists"] = True
    except Program.DoesNotExist:
        context["failed"] = True

    context["programs"] = Program.objects.filter(department__code=dept_code)
    context["dept_code"] = dept_code
    return render(
        request, "organization/partials/dept_prog_list.html", context, status=200
    )


@user_passes_test(lambda u: u.groups.filter(name="Counselor").exists())
def delete_department(request):
    context = {}
    checked = request.POST.getlist("department_id")
    edu_level_id = request.POST["edu_level"]
    Department.objects.filter(educationlevel__id=edu_level_id, id__in=checked).delete()
    context["yearlevels"] = Year.objects.filter(educationlevel__id=edu_level_id)
    context["departments"] = Department.objects.filter(educationlevel__id=edu_level_id)
    return render(request, "organization/partials/department_list.html", context)


@user_passes_test(lambda u: u.groups.filter(name="Counselor").exists())
def delete_program(request):
    context = {}
    checked = request.POST.getlist("program")
    dept_code = request.POST["dept_code"]
    edu_level_id = request.POST["edu_level_id"]
    if dept_code:
        dept = Department.objects.get(educationlevel__id=edu_level_id, code=dept_code)   
        Program.objects.filter(department=dept, id__in=checked).delete()
        context["programs"] = Program.objects.filter(department=dept)
    return HttpResponse("")


def handle_edu_levels_select(request):
    context = {}
    try:
        edu_level_id = request.GET.get("edu_level_id")
        if edu_level_id.isnumeric():
            education_level = EducationLevel.objects.get(id=edu_level_id)
            context["departments"] = Department.objects.filter(
                educationlevel=education_level
            )
            context["yearlevels"] = Year.objects.filter(educationlevel=education_level)
    except EducationLevel.DoesNotExist:
        pass
    return render(request, "organization/partials/department_list.html", context)

@user_passes_test(lambda u: u.groups.filter(name="Counselor").exists())
def add_yearlevel(request):
    context = {}
    edu_level_id = request.POST["edu_level_id"]
    yearlevel = request.POST["yearlevel_name"]
    edu_level = EducationLevel.objects.get(id=edu_level_id)

    try:
        if not Year.objects.filter(educationlevel=edu_level, name=yearlevel):
            new_yearlevel = Year()
            new_yearlevel.educationlevel = edu_level
            new_yearlevel.name = yearlevel
            new_yearlevel.save()
            context["success"] = True

        context["yearlevels"] = Year.objects.filter(educationlevel=edu_level)
        context["yearlevel_table"] = Year.objects.filter(educationlevel=edu_level)
    except:
        context["failed"] = True
    return render(request, "organization/partials/yearlevel_list.html", context)

def delete_yearlevel(request):
    context = {}
    checked = request.POST.getlist("checked")
    edu_level_id = request.POST["edu_level_id"]
    edu_level = EducationLevel.objects.get(id=edu_level_id)
    Year.objects.filter(educationlevel=edu_level, id__in=checked).delete()

    context["yearlevels"] = Year.objects.filter(educationlevel=edu_level)
    context["yearlevel_table"] = Year.objects.filter(educationlevel=edu_level)
    return render(request, "organization/partials/yearlevel_list.html", context)
