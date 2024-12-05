from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Redirecionamento após login
LOGIN_REDIRECT_URL = '/'  
LOGOUT_REDIRECT_URL = '/accounts/login/'  
LOGIN_URL = 'login'
LOGOUT_URL = 'logout'





# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-8dti0jh^hm-e4bx(sn^p!u00-=#8q8^31##n8rw#t#%++%u1^*"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "core",
    "storages",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware", 
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "dataroomcloud.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "core" / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "dataroomcloud.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'dbdataroomcloud',      
        'USER': 'mysuperuser',            
        'PASSWORD': 'mysuperuser',          
        'HOST': 'db-dataroom-cloud.cpknuxiwuthi.us-east-1.rds.amazonaws.com',          
        'PORT': '5432',               
    }
}



# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

TIME_ZONE = 'America/Sao_Paulo'
LANGUAGE_CODE = 'pt-br'


USE_I18N = True

USE_TZ = True

AUTH_USER_MODEL = 'core.Usuario'



STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3.S3Storage",
        "OPTIONS": {
            "access_key": "AKIARNHLSARVIXWGV4T7",
            "secret_key": "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",
            "bucket_name": 'dataroomclouds3',
            "region_name": 'us-east-1',
            "default_acl": None,
            "querystring_auth": False,  
        },
    },
     "staticfiles": {
        "BACKEND": "storages.backends.s3.S3Storage",
        "OPTIONS": {
            "access_key": "AKIARNHLSARVIXWGV4T7",
            "secret_key": "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",
            "bucket_name": 'dataroomclouds3',
            "region_name": 'us-east-1',
            "default_acl": None,
            "location": 'staticfiles/',  
            "querystring_auth": False,
        },
    },
}

STATIC_URL = "https://dataroomclouds3.s3.amazonaws.com/staticfiles/"
MEDIA_URL = "https://dataroomclouds3.s3.amazonaws.com/"
STATICFILES_STORAGE = "storages.backends.s3.S3Storage"


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
        'storages': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
        'boto3': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
        'botocore': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}
