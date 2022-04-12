from .common import *

DEBUG = False
ALLOWED_HOSTS = ["jmcproject.herokuapp.com", "127.0.0.1", "localhost"]

SECRET_KEY = os.environ["SECRET_KEY"]

DATABASES = {
    # production
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'd185ibt8phh2o8',
        'USER': os.environ['DB_USER'],
        'PASSWORD': os.environ['DB_PASS'],
        'HOST':'ec2-18-235-114-62.compute-1.amazonaws.com',
        'PORT': '5432',
    }
}