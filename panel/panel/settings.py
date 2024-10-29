from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent



# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-h-l4)eixka@39jr!yvtce46@cwx#w&&(7_p5d*hqszkp+k5_gu'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost','127.0.0.1','0.0.0.0','23.88.54.241']


# Application definition

INSTALLED_APPS = [
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'link',
    'order',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'django_filters',
    'corsheaders',
    'gunicorn',
    'whitenoise',
    'celery',
    'redis'
]


CELERY_BROKER_URL = "redis://redis:6379/0"
CELERY_RESULT_BACKEND = "redis://redis:6379/0"
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'




MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'panel.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'panel.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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



REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        #"accounts.backends.JWTAuthentication",
        'allauth.account.auth_backends.AuthenticationBackend',
    )
}


AUTHENTICATION_BACKENDS = ['django.contrib.auth.backends.ModelBackend',]
''' 
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]
'''

SITE_ID = 1


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = "smtp.c1.liara.email"
EMAIL_PORT = 587
EMAIL_HOST_USER = "happy_rosalind_po1nl8"
EMAIL_HOST_PASSWORD = "8933acf5-9f14-423e-b179-84852ec9f865"
EMAIL_USE_TLS = True  # Use TLS encryption
EMAIL_FROM_ADDRESS = "contact@helpfinity.app"


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = "/static/"
MEDIA_ROOT =BASE_DIR/"media"
MEDIA_URL = "/media/"
STATICFILES_DIRS = ["docs/"]

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


#CORS_REPLACE_HTTPS_REFERER = True
#CORS_ALLOW_CREDENTIALS = True
#CORS_ALLOWED_ORIGINS = ["http://localhost","http://127.0.0.1",'http://23.88.54.241:8000']
CSRF_TRUSTED_ORIGINS = ["http://localhost","http://127.0.0.1",'http://23.88.54.241:8000']
CORS_ORIGIN_WHITELIST = ["http://localhost","http://127.0.0.1",'http://23.88.54.241:8000']
#CORS_ORIGIN_ALLOW_ALL = True
SESSION_COOKIE_SECURE=False
CSRF_COOKIE_SECURE = False
