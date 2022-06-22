from psytests.settings.dev import DATABASES
from .common import *
import dj_database_url

DEBUG = False
ALLOWED_HOSTS = ["psytest-app.herokuapp.com", "jmcproject.herokuapp.com"]

SECRET_KEY = os.environ["SECRET_KEY"]

SITE_ID = 3

DATABASES = {
    'default': dj_database_url.config(conn_max_age=500, ssl_require=True)
}

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
