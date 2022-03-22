"""
Django settings for EMedix project.

Generated by 'django-admin startproject' using Django 3.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
import os



# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent




# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'acm2&mkcm%$qhipc&-s8_7ic)n1wglebdeat7v9(6iuow_#u_6'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True #not os.getenv('GAE_APPLICATION', None)

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'sslserver',
    #Custom Apps
    'EMedix_App',
    'video_app',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django_session_timeout.middleware.SessionTimeoutMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'EMedix.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'EMedix.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

#STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

#STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATICFILES_DIRS = [ BASE_DIR / "static" ]


MEDIA_URL = '/media/'
#MEDIA_ROOT = '/files'
#MEDIA_ROOT = '/home'
#os.path.join(BASE_DIR, 'media')
MEDIA_ROOT = BASE_DIR / "media"

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = "infoemedixhealthcare@gmail.com"
#FOR LOCAL 
EMAIL_HOST_PASSWORD = "ebcbbpnhvzcysrcs"
#FOR PRODUCTION
#EMAIL_HOST_PASSWORD = "jupjhmrooqtybjvy"



SESSION_EXPIRE_SECONDS = 600  # 10 mins
SESSION_EXPIRE_AFTER_LAST_ACTIVITY = True
SESSION_TIMEOUT_REDIRECT = '/login'

STRIPE_PUBLISHABLE_KEY = 'pk_test_51J4qzoHuUPRqQPVoJGxKTzo2JAYKRj9lDU2JG930uX7682QTvyGeki1t5GwV5Kl7zIMrad85zFs5uWHSDIEfZmDi00muK2YpNb'
STRIPE_SECRET_KEY = 'sk_test_51J4qzoHuUPRqQPVo9bJB6ijcsAHgHH1qaFjImrEyd1uk3oC0dxmWeJPqvZBsYyoQPUXI1PJNi39j0QZipj8AT3Ha007HOEl1V3'


X_FRAME_OPTIONS = 'ALLOWALL'

XS_SHARING_ALLOWED_METHODS = ['POST','GET','OPTIONS', 'PUT', 'DELETE']



TWILIO_ACCOUNT_SID = 'AC59ebf735dd3580c10983bbcbaeddff84'
TWILIO_API_KEY_SID = 'SK6bcf74b192cfc0f8bbe435a3003a9373'
TWILIO_API_KEY_SECRET = 'GfeWslRhOZlBrcXrkSYyugLVMleIXupE' 
