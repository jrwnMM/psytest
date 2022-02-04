from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.shortcuts import render,redirect, reverse
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from .forms import CreateUserForm,UpdateUserForm
from django.views.generic import (
    UpdateView,)

# Create your views here.

from datetime import datetime

UserModel = get_user_model()
now = datetime.today()

def loginPage(request):
    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')

        user=authenticate(request,username=username,password=password)
        
        if user is not None:
            login(request,user)
            return HttpResponseRedirect(reverse('homepage'))
        else:
            messages.error(request, 'Username or Password is incorrect')
    return render(request,'accounts/login.html')

def registerPage(request):
    if request.method == 'POST':
        form=CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            user.refresh_from_db()
            user.profile.date_of_birth = form.cleaned_data.get('date_of_birth')
            user.profile.gender = form.cleaned_data.get('gender')
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
        form = CreateUserForm()
    context = {'form': form}
    return render(request,'accounts/register.html',context)


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

class editProfile(UpdateView):
    model = User
    form_class = UpdateUserForm
    template_name = 'accounts/profile.html'
    success_url = reverse_lazy('homepage')

    def get_object(self):
        return self.request.user


