from .common import *
import dj_database_url

DEBUG = False
DEBUG_PROPAGATE_EXCEPTIONS = True
ALLOWED_HOSTS = ["https://psytestjmc.up.railway.app/", "psytestjmc.up.railway.app"]

SECRET_KEY = os.environ["SECRET_KEY"]

SITE_ID = 1

DATABASES = {
    'default': dj_database_url.config(conn_max_age=500, ssl_require=True)
}

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
