from pathlib import Path
from dotenv import load_dotenv
import os
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    # local
    "accounts.apps.AccountsConfig",
    "administration.apps.AdministrationConfig",
    "riasec.apps.RiasecConfig",
    "userprofile.apps.UserprofileConfig",
    "personalityTest.apps.PersonalitytestConfig",
    "evaluation.apps.EvaluationConfig",
    "iqtest.apps.IqtestConfig",
    # allauth
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    # providers
    "allauth.socialaccount.providers.google",
    "allauth.socialaccount.providers.facebook",
    #filters
    "django_filters",
    "mathfilters",
    #Other apps
    'django_quill',
    'widget_tweaks',
    "phonenumber_field",
    "django_htmx",
]


AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
    "psytests.auth.EmailBackend",
)
SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "SCOPE": [
            "profile",
            "email",
        ],  
        "AUTH_PARAMS": {
            "access_type": "online",
        },
        "APP": {
            "client_id": os.environ["GOOGLE_CLIENT_ID"],
            "secret": os.environ["GOOGLE_SECRET_KEY"],
        },
    },
    "facebook": {
        "SCOPE": [
            "profile",
            "email",
        ],
        "AUTH_PARAMS": {
            "access_type": "online",
        },
        "APP": {
            "client_id": os.environ["FB_CLIENT_ID"],
            "secret": os.environ["FB_SECRET_KEY"],
        },
    },
}

ACCOUNT_AUTHENTICATION_METHOD = "email"  # Defaults to username_email
ACCOUNT_USERNAME_REQUIRED = False  # Defaults to True
ACCOUNT_EMAIL_REQUIRED = True  # Defaults to False
SOCIALACCOUNT_QUERY_EMAIL = ACCOUNT_EMAIL_REQUIRED
SOCIALACCOUNT_AUTO_SIGNUP = True
SOCIALACCOUNT_EMAIL_REQUIRED = False
ACCOUNT_ADAPTER = "psytests.adapter.MyLoginAccountAdapter"
SOCIALACCOUNT_ADAPTER = "psytests.adapter.MySocialAccountAdapter"

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_htmx.middleware.HtmxMiddleware",
]

ROOT_URLCONF = "psytests.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / "templates",
            BASE_DIR / "administration" / "organization" / "templates",
            BASE_DIR / "administration" / "usermanagement" / "templates",
            BASE_DIR / "administration" / "userstocheck" / "templates",
            BASE_DIR / "administration" / "userschedules" / "templates",
            BASE_DIR / "administration" / "statistics" / "templates",
            BASE_DIR / "administration" / "career" / "templates",
            BASE_DIR / "administration" / "personality" / "templates", 
            BASE_DIR / "administration" / "iq" / "templates",
            ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "social_django.context_processors.backends",
                "social_django.context_processors.login_redirect",
                "psytests.context_processors.check_role",
            ],
        },
    },
]

WSGI_APPLICATION = "psytests.wsgi.application"


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Manila"

USE_I18N = True

USE_L10N = True

USE_TZ = False


STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = "/images/"
MEDIA_ROOT = os.path.join(BASE_DIR, "static/images")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGIN_URL = "accounts:login"
LOGIN_REDIRECT_URL = "homepage"
LOGOUT_REDIRECT_URL = "homepage"

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = os.environ["EMAIL_HOST_USER"]
EMAIL_HOST_PASSWORD = os.environ["EMAIL_HOST_PASSWORD"]

QUILL_CONFIGS = {
    'default':{
        'theme': 'snow',
        'modules': {
            'syntax': True,
            'toolbar': [
                [
                    {'font': []},
                    {'header': []},
                    {'align': []},
                    'bold', 'italic', 'underline', 'strike', 'blockquote',
                    {'color': []},
                    {'background': []},
                ],
                [{ 'list': 'ordered'}, { 'list': 'bullet' }],
                ['code-block', 'link'],
                ['clean'],
            ]
        }
    }
}