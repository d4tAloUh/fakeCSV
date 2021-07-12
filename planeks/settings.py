import os
import django_heroku
import firebase_admin

from pathlib import Path
from firebase_admin import storage, credentials

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-z+fu^l9801@efldo%bt+8lsbrnr#o7mjfe=&w35i!=5fhia+-e')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'True') == 'True'

ALLOWED_HOSTS = ['fake-csv-d4t-alouh.herokuapp.com', '127.0.0.1', 'localhost']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # apps
    'fakeCSV.apps.FakecsvConfig'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'planeks.urls'

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

WSGI_APPLICATION = 'planeks.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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

AUTH_USER_MODEL = 'fakeCSV.CustomUser'

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Europe/Kiev'
USE_I18N = True
USE_L10N = False
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static_files/'

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# django auth
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'user-schemas'
LOGOUT_REDIRECT_URL = '/'

# CELERY
CELERY_BROKER_URL = os.environ.get('REDISTOGO_URL', 'redis://localhost:6379')
CELERY_RESULT_BACKEND = CELERY_BROKER_URL


credential = credentials.Certificate({
    "type": "service_account",
    "project_id": "planeks-test-4227a",
    "private_key_id": os.environ.get("private_key_id", "32a7264e24815e99a33e14c2743dac11f4d9f1e4"),
    "private_key": os.environ.get("private_key",
                                  "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDAH1XtzFd4ZCPX\nsrSl+/QOHEPbJ955ASjo0FOAl1St8l6GwlRyODrk3cxZRxN4RPKkJ5+nBw4TNPky\nsaSaHJnG6tgSqdgiVAG7vS+647Zp4tV1dDNgBySFOyguk1FFyK3/3gLmBwpRxb7H\nw70JN8Jw/NsgwBY0TCCkafVqBmDLLOuZEaHpBYMGbwEedA/RFCqdUxtzrExe0DMn\n4tpU1Zo9aX5nfoHHcDbNlI8WP0mShZSi1B3eV64jEBcKDJT17TYstLlmHnT2O3Wi\nr+TqpIvCRMDTWlukbwoBFVXcGe85NyMQXleOZ2zGUPGupmXW4IJw9fSnuHKBYryJ\nvLQgApjnAgMBAAECggEACMkGCrnhir74Mp4DNmSHPE6c6Gcc0by0rFy7t3F0F6uH\nGLNx3XKRIt5k60oy644qPZ5q5bOOuGB06sAGeQjzcTio88WHfXOzoUGdQ/cIuYkm\ns1htHFLcn9OyL9sLCDK33i+T7gUxZXGHmqaVPNgrZd5Hfj+6ZDQno/e3wgbo+Ia7\niVH+qKzFLYWA4/jsSwjL07VPlqPP5KPa3zurC01LczhtnZmEURqgK/RFtSyUcQyG\n5pPqu560m94thiwpEDUrjR30lPaA1E8dAHdMuI4IQleWOMwVXPJa9Wx5PXrHEWFB\nUTDo3HRV289byd7Rk4Wg1XjDb6g6KlRY14Mnd7DigQKBgQDkdZ4hhvFj45jmcgqa\nqjj43NZBOAj1pe4BiNWBqmr954dhmZzvDHO9hJ+Krj7Uzkmk+/Ig1NZpAlkZIejL\nlvqPhWo5075+NQwHZSWFzJ2dBBMQSsz6JAKycfUGt0JmWZ6XgS8KVeU6aGiAxZI0\nsreCP9A5lOjlir4sO1EKFBiMgQKBgQDXSFZUxi/PuWiDa0OT/kljZZXXi9v1HZ6Q\n3GlH9CaT64NOcnd4VqWhp66r3o8stw2ZIyzg2B8HFv6oOb8GD7KW981V/eMmQHxF\nX2nlB/OzIMk2D2yUK2EzzLyQLwUh7LWSgv4X3wK7fNO0BQDR0n33fAbqO+n51LM9\n7WiFAA2RZwKBgQDHGcYNHAhlcGXBd+PL9Muf/v3uasJMKyaoSbMgxP9ndg7jPTeq\nkWSQ5vMPrlltprZBxZy3hiWx8Gzr3UR/oX2N9MylxuZ+IQbxrvGrkK5Pt8xRZ48J\n9LYxA+Vxy+ZfQn1XNitjy4XxiCqDBywrJxGMvsZeWGs8GNUxwSQYL3lRgQKBgF2n\n457nxV8KGxSpMnIMuyKZzBFEkAFXzGba7JZX+fx6Bdq344+fqljkWRH+Na1PSYQo\nkFqUyxLLhyfqT1c0tw4EafkSBaLbhPStKKVxyyxPhBmXpjXjlVryo8naGtKCZw+B\nG0eJRmgISxVS4+NkPlbPRzbZr9V3Gi9DvCe4OS7bAoGAIoGHEtye+Q/4FHFKxDv5\n/xK0ltiQHSqnezP0MqRk83k1EeiPvYpM+umdpoe7eoMTYaVZd993gbl91I+jU9KZ\nBk7fg4modwh2zRIlnqrCCnVR4r6BhDw0Z9cPZf9iFZqEo8/FvJ1lx0WoANbHZo9b\npq5F3ONJzZtlBxwtmFU9cJA=\n-----END PRIVATE KEY-----\n"),
    "client_email": os.environ.get('client_email',
                                   "firebase-adminsdk-9fo2f@planeks-test-4227a.iam.gserviceaccount.com"),
    "client_id": os.environ.get('client_id', "108400431971091242931"),
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-9fo2f%40planeks-test-4227a.iam.gserviceaccount.com"
})

firebase_app = firebase_admin.initialize_app(credential, {
    'storageBucket': "planeks-test-4227a.appspot.com"
})

bucket = storage.bucket(app=firebase_app)


django_heroku.settings(locals())


