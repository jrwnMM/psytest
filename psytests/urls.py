"""psytests URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import  settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView
from django.contrib.staticfiles.storage import staticfiles_storage
from accounts.forms import CustomizedPasswordResetForm, CustomizedPasswordResetConfirmForm
from psytests.views import Assessment, DataPrivacyConsent, HomePageView, Awesome, request_counsel

from django.contrib.auth import views as auth_views


urlpatterns = [
    path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('icons/favicon.ico'))),
    path('admin/', admin.site.urls),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name = 'accounts/password_reset_form.html', email_template_name='accounts/password_reset_email.html', form_class=CustomizedPasswordResetForm), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html', form_class=CustomizedPasswordResetConfirmForm), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'), name='password_reset_complete'),
    path('', HomePageView.as_view(), name="homepage"),
    path('assessment/', Assessment.as_view(), name="assessment"),
    path('awesome/', Awesome.as_view(), name="awesome"),
    path('<str:test>/data/privacy/consent', DataPrivacyConsent.as_view(), name="consent"),
    path('profile/', include('userprofile.urls')),
    path('evaluation/', include('evaluation.urls')),
    path('auth/', include('accounts.urls')), #Connects to psytest folder urls.py
    path('career/',include('riasec.urls')), #Connects to riasec folder urls.py
    path('personality/',include('personalityTest.urls')), #Connects to personalityTest folder urls.py
    path('accounts/', include('allauth.urls')),
    path('administration/', include('administration.urls')),
    path('request-counsel/', request_counsel, name='request-counsel'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)