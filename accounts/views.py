from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from .forms import CreateUserForm, UpdateUserForm
from django.views.generic import (
    UpdateView, TemplateView)
from .models import Department, Program, Year, Profile
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.sites.models import Site
# Create your views here.


UserModel = get_user_model()


def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('homepage'))
        else:
            messages.error(request, 'Username or Password is incorrect')
    else:
        if request.user.is_authenticated:
            return redirect('homepage')
        else:
            return render(request, 'accounts/login.html')


def registerPage(request):
    form = CreateUserForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            user.refresh_from_db()
            user.profile.middle_name = form.cleaned_data.get('middle_name')
            user.profile.date_of_birth = form.cleaned_data.get('date_of_birth')
            user.profile.gender = form.cleaned_data.get('gender')
            user.profile.contactNumber = form.cleaned_data.get('contactNumber')
            user.profile.department = Department.objects.get(name=request.POST.get("department"))
            user.profile.program = Program.objects.get(name=request.POST.get("program"))
            user.profile.year= Year.objects.get(name=request.POST.get("year"))
            user.save()

            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('accounts/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            return render(request, 'accounts/emailConfirmationView.html')
        else:
            print('Printing...', form.errors)
    else:
        if request.user.is_authenticated:
            return redirect('homepage')
    context = {
        'form': form,
        'department': [('', 'Please Select One')] + Department.departments,
        'program_ibed': [('', 'Please Select One')] + Program.programs[0][1],
        'program_college': [('', 'Please Select One')] + Program.programs[1][1],
        'year_grade': [('', 'Please Select One')] + Year.years[0][1],
        'year_junior': [('', 'Please Select One')] + Year.years[1][1],
        'year_senior': [('', 'Please Select One')] + Year.years[2][1],
        'year_college': [('', 'Please Select One')] + Year.years[3][1],
        }
    return render(request, 'accounts/register.html', context)


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = UserModel._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, 'accounts/emailActivatedView.html')
    else:
        return render(request, 'accounts/emailActivationInvalidView.html')


def logoutUser(request):
    logout(request)
    return redirect('accounts:login')


# def editProfile(request):
#     if request.method == 'POST':
#         form = UpdateUserForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.profile.date_of_birth = form.cleaned_data.get('date_of_birth')
#             # user.profile.gender = form.cleaned_data.get('gender')
#             user.first_name=form.cleaned_data.get('first_name')
#             user.last_name=form.cleaned_data.get('last_name')
#             user.username=form.cleaned_data.get('username')
#             user.is_superuser=form.cleaned_data.get('is_superuser')
#             user.email=form.cleaned_data.get('email')
#             user.profile.department = form.cleaned_data.get('department')
#             user.profile.program = form.cleaned_data.get('program')
#             user.profile.year = form.cleaned_data.get('year')
#             user.profile.save()
#             user.save()
#
#         return redirect('homepage')
#
#     else:
#         form = UpdateUserForm()
#         try:
#             initial = Profile.objects.get(user=request.user)
#         except ObjectDoesNotExist:
#             pass
#         context = {'form': form, 'initial': initial, 'department': Department.objects.all(),
#                    'program': Program.objects.all(), 'year': Year.objects.all(),}
#
#         return render(request, 'accounts/profile.html', context)

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = Profile.objects.get(user=self.request.user)
        return context

class EditProfile(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UpdateUserForm
    template_name = 'accounts/profile-edit.html'
    success_url = reverse_lazy('accounts:profile')

#ValueError
    def get_context_data(self, **kwargs):
        context = super(EditProfile, self).get_context_data(**kwargs)
        context['initial']=Profile.objects.get(user=self.request.user)
        context['department']=Department.objects.all()
        context['program']=Program.objects.all()
        context['year']=Year.objects.all()
        return context

    def get_form_kwargs(self):
        department = [
            ('IBED', 'Integrated Basic Education (Preschool to SHS)'),
            ('College', 'College Department')
        ]
        program = [
            ('Grade', 'Grade School'),
            ('Junior', 'Junior Highschool'),
            ('Senior', 'Senior Highschool'),
            ('BSA', 'BS in Accountancy'),
            ('BSBA', 'BS in Business Administration'),
            ('BSMA', 'BS in Management Accounting'),
            ('BSC', 'BS in Criminology'),
            ('BSCE', 'BS in Civil Engineering'),
            ('BSE', 'Bachelor in Secondary Education'),
            ('BEE', 'Bachelor in Elementary Education'),
            ('BSIT', 'BS in Information Technology'),
            ('BSP', 'BS in Psychology'),
            ('BSSW', 'BS in Social Work'),
            ('BSMT', 'BS in Medical Technology'),
        ]
        year = [
            ('1', 'Grade 1'),
            ('2', 'Grade 2'),
            ('3', 'Grade 3'),
            ('4', 'Grade 4'),
            ('5', 'Grade 5'),
            ('6', 'Grade 6'),
            ('7', 'Grade 7'),
            ('8', 'Grade 8'),
            ('9', 'Grade 9'),
            ('10', 'Grade 10'),
            ('11', 'Grade 11'),
            ('12', 'Grade 12'),
            ('1st', '1st Year'),
            ('2nd', '2nd Year'),
            ('3rd', '3rd Year'),
            ('4th', '4th Year'),
            ('5th', '5th Year'),
        ]
        gender = [
        ('', '---'),
        ('M', 'Male'),
        ('F', 'Female'),
    ]
        kwargs = super(EditProfile, self).get_form_kwargs()
        kwargs['gender'] = gender
        kwargs['department'] = department
        kwargs['program'] = program
        kwargs['year'] = year
        return kwargs

    def form_valid(self, form):
        user = form.save(commit=False)
        user.refresh_from_db()
        user.profile.date_of_birth = form.cleaned_data.get('date_of_birth')
        user.profile.gender = form.cleaned_data.get('gender')
        user.first_name = form.cleaned_data.get('first_name')
        user.last_name = form.cleaned_data.get('last_name')
        #---------------------
        user.profile.middle_name = form.cleaned_data.get('middle_name')
        user.profile.contact = form.cleaned_data.get('contact')
        #---------------------
        user.username = form.cleaned_data.get('username')
        user.is_superuser = form.cleaned_data.get('is_superuser')
        user.profile.department = Department.objects.get(name=form.cleaned_data.get('department'))
        user.profile.program = Program.objects.get(name=form.cleaned_data.get('program'))
        user.profile.year = Year.objects.get(name=form.cleaned_data.get('year'))
        user.save()
        return super().form_valid(form)


