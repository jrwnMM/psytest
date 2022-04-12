from .common import *

DEBUG = True
DEBUG_PROPAGATE_EXCEPTIONS = True

SECRET_KEY = 'django-insecure-enn_1_qy&r1^^fqcus4@s^mb5&5%bg1--mogq=b**8be^w)l$0'

DATABASES = {
    # local
    # "default": {
    #     "ENGINE": "django.db.backends.postgresql",
    #     "NAME": os.environ["LOCAL_DB_NAME"],
    #     "USER": os.environ["LOCAL_DB_USER"],
    #     "PASSWORD": os.environ["LOCAL_DB_PASS"],
    #     "PORT": "5432",
    # }
    # local-test
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": 'psytest-test',
        "USER": os.environ["LOCAL_DB_USER"],
        "PASSWORD": os.environ["LOCAL_DB_PASS"],
        "PORT": "5432",
    }
}