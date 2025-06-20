"""
Django settings for login project.

Generated by 'django-admin startproject' using Django 5.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
import os
from decouple import config


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)


ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

AUTH_USER_MODEL = 'users.CustomUser'
  # Correct format


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    "django.contrib.auth",
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'patent',
    'copyright',
    'sldc',
    'GI',
    'design',
    'trademark',
    'users',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'csp.middleware.CSPMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'users.middleware.TrackPageViewsMiddleware',
]


# Session settings
SESSION_ENGINE = 'django.contrib.sessions.backends.db'  # Store sessions in the database
SESSION_COOKIE_NAME = 'sessionid'  # Default session cookie name
SESSION_COOKIE_AGE = 3600  # Session expires after 1 hour (in seconds)
SESSION_EXPIRE_AT_BROWSER_CLOSE = False  # Keep session even after browser is closed
SESSION_COOKIE_SECURE = False  # Set to True if using HTTPS
SESSION_COOKIE_HTTPONLY = True  # Prevent client-side access to the session cookie
SESSION_SAVE_EVERY_REQUEST = True


X_FRAME_OPTIONS = 'DENY'  # Prevent iframe embedding
SECURE_BROWSER_XSS_FILTER = True  # Enable XSS protection

SECURE_CONTENT_TYPE_NOSNIFF = True  # Prevents MIME-type sniffing attacks

CSP_DEFAULT_SRC = ["'self'"]  # Allow resources only from the same origin
CSP_SCRIPT_SRC = ["'self'"]  # Restrict JavaScript loading
CSP_STYLE_SRC = ["'self'"]  # Restrict CSS loading
CSP_IMG_SRC = ["'self'"]  # Allow images only from your domain
CSP_FRAME_ANCESTORS = ["'none'"]  # Prevent clickjacking

CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True

SECURE_SSL_REDIRECT = False  # Forces HTTPS
SECURE_HSTS_SECONDS = 31536000  # Ensures max-age is at least one year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True  # Applies to all subdomains
SECURE_HSTS_PRELOAD = True  # Allows browser preload lists


ROOT_URLCONF = 'login.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'login.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases


DATABASES = {
    'default': {
        # 'ENGINE': 'mysql.connector.django',
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT'),
    }
}
print("DB_HOST:", config("DB_HOST")) 



# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators


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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

LOGIN_REDIRECT_URL = 'users:home'  # Redirect to this after successful login
LOGOUT_REDIRECT_URL = 'users:login'  # Redirect after logout
LOGIN_URL = '/not-logged-in/'  # Redirect here when a user is not logged in

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'users/static')]  # Path to your static folder
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',  # Keep Django's default backend as fallback
]

