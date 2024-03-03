# settings.py
# gfg/settings.py

import os
from pathlib import Path

# APPEND_SLASH=True
APPEND_SLASH=False

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-atrwia7n9xb9(!&k#3l-q+&ll^toqmw&qvx285uj+9(_c9v^88'

DEBUG = True
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',  
    'django.contrib.staticfiles',
    'social_django',
    'gfg',
    'authentication',
    'rest_framework',
    'django_celery_beat',

]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
]



ROOT_URLCONF = 'gfg.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ["templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
            ],
        },
    },
]

WSGI_APPLICATION = 'gfg.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'fitness',
        'USER': 'root',
        'PASSWORD': 'Hemant12@',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}


import os 

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'templates/static'),
]
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR,'staticfiles')


EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'kavypatel255@gmail.com'
EMAIL_HOST_PASSWORD = 'arvpsghuyrhcjkrx'  # Add your email password here
EMAIL_PORT = 587

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'

#  i want to set india kolkata time

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = True

AUTHENTICATION_BACKENDS = [
    'social_core.backends.google.GoogleOAuth2',
    'django.contrib.auth.backends.ModelBackend',
]

LOGIN_URL = 'signin'
LOGIN_REDIRECT_URL = 'home'
LOGOUT_URL = 'signout'
LOGOUT_REDIRECT_URL = 'signin'

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '1051432913097-ikjdil1egkg893l9hdidjicomk99fre5.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = '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'
SOCIAL_AUTH_GOOGLE_OAUTH2_REDIRECT_URI = 'http://localhost:8000/complete/google-oauth2/'
SOCIAL_AUTH_URL_NAMESPACE = 'social'
SOCIAL_AUTH_GOOGLE_OAUTH2_IGNORE_DEFAULT_SCOPE = True
SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = ['email','profile','https://www.googleapis.com/auth/fitness.activity.read']
CORS_ALLOW_ALL_ORIGINS = True
CORE_ORIGIN_ALLOW_ALL = True
CORE_ALLOW_CREDENTIALS=True


