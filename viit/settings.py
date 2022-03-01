import os
import environ
import datetime
env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)
# reading .env file
environ.Env.read_env()

# False if not in os.environ
DEBUG = env('DEBUG')

# Raises django's ImproperlyConfigured exception if SECRET_KEY not in os.environ
SECRET_KEY = env('SECRET_KEY')

JWT_SECRET_KEY = env('JWT_SECRET_KEY')

JWT_AUTH = {
    # how long the original token is valid for
    'JWT_EXPIRATION_DELTA': datetime.timedelta(hours=5),

    # allow refreshing of tokens
    'JWT_ALLOW_REFRESH': True,

    # this is the maximum time AFTER the token was issued that
    # it can be refreshed.  exprired tokens can't be refreshed.
    'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(hours=5),
}


FRONTEND_URL = env('FRONTEND_URL')
BACKEND_URL =  env('BACKEND_URL')

# Parse database connection url strings like psql://user:pass@127.0.0.1:8458/db
DATABASES = {
    # read os.environ['DATABASE_URL'] and raises ImproperlyConfigured exception if not found
    'default': env.db(),
}


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


ALLOWED_HOSTS = ["*"]

# Mail Configurations
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtpout.secureserver.net'
#EMAIL_USE_TLS = True
EMAIL_USE_SSL = True
EMAIL_PORT = 465
EMAIL_HOST_USER = 'Info@shreeenterprise.org '#'webmasteritdude@gmail.com'
EMAIL_HOST_PASSWORD = 'shree@123'#'A7507398717D'
DEFAULT_FROM_EMAIL=EMAIL_HOST_USER



# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_auth',
    'rest_framework',
    'corsheaders',
    'rest_framework_simplejwt',
    'b2c',
    'admin_dashboard',
    'b2c.adds',
    'b2c.search',
]


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
]

CORS_ORIGIN_WHITELIST = [
    env('FRONTEND_URL'),
]

# CORS_ALLOW_METHODS = [ 'DELETE', 'GET', 'OPTIONS', 'PATCH', 'POST', 'PUT', ]

ROOT_URLCONF = 'viit.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.dirname(BASE_DIR), 'templates'],
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

WSGI_APPLICATION = 'viit.wsgi.application'



AUTH_USER_MODEL = 'rest_auth.User'
# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'

MEDIA_URL = '/media/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

LOGIN_URL = "/admin_dashboard/admin_login/"

STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'static')

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
