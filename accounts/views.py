from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from .forms import CreateUserForm
from .models import Department, EducationLevel, Program, Year
from django.db import transaction
# Create your views here.


User = get_user_model()


def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('homepage')
        else:
            messages.error(request, 'Username or Password is incorrect')
    else:
        if request.user.is_authenticated:
            return redirect('homepage')

    return render(request, 'accounts/login.html')

@transaction.atomic
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
            user.profile.educationlevel = get_or_none(EducationLevel, id=request.POST.get("educationlevel"))
            user.profile.department = get_or_none(Department, id=request.POST.get("department"))
            user.profile.program = get_or_none(Program, id=request.POST.get("program") or None)
            user.profile.year= get_or_none(Year, id=request.POST.get("year"))
            user.save()
            user.profile.save()


            if user.email:
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
                user.is_active = True
                user.save()
                return redirect('homepage')
    else:
        if request.user.is_authenticated:
            return redirect('homepage')
    context = {
        'form': form,
        }
    return render(request, 'accounts/register.html', context)

def get_or_none(classmodel, **kwargs):
    try:
        return classmodel.objects.get(**kwargs)
    except classmodel.DoesNotExist:
        return None

def departments(request):
    form=CreateUserForm(request.GET)
    return HttpResponse(form['department'])

def programs(request):
    form=CreateUserForm(request.GET)
    return HttpResponse(form['program'] or '')

def years(request):
    form = CreateUserForm(request.GET)
    response = HttpResponse(form['year'] or None)
    return response
        

@transaction.atomic
def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
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




