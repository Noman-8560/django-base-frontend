import os
import environ

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

""" CONFIGURATIONS -----------------------------------------------------------------------------------------------"""

AUTH_USER_MODEL = 'accounts.User'
ROOT_URLCONF = 'cocognite.urls'
WSGI_APPLICATION = 'cocognite.wsgi.application'
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

env_file = os.path.join(BASE_DIR, ".env")
env = environ.Env()
env.read_env(env_file)

SECRET_KEY = 's(l5vi&5nq3619gdskadhgjaksd981234hlaskhjdlasd'
ZOOM_API_KEY_JWT = 'EBB0k1HnRN6hlD5dvrkAyw'
ZOOM_API_SECRET_JWT = '1hnrKhnDfgbZDsg5WdLKxEIA9bZsPBm2BKOF'

USE_TESTING_DB_SERVER = env('USE_TEST_DB_SERVER') == 'True'
DEBUG = True
SERVER = False
TEST = False
ALLOWED_HOSTS = ['*']

if TEST:
    GOOGLE_CALLBACK_ADDRESS = "https://tasktok.app/accounts/google/login/callback"
    SITE_ID = 2
else:
    GOOGLE_CALLBACK_ADDRESS = "http://127.0.0.1:8000/accounts/google/login/callback"
    SITE_ID = 1

CRISPY_TEMPLATE_PACK = 'bootstrap4'
LOGIN_REDIRECT_URL = '/accounts/cross-auth/'

""" INSTALLATIONS ------------------------------------------------------------------------------------------------"""

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # REQUIRED_APPLICATIONS
    'crispy_forms',
    'ckeditor',

    # TEMP
    'django_seed',

    # AUTH_API
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',

    # SESSION_APP
    'preventconcurrentlogins',

    # USER_APPLICATIONS
    'src.application',
    'src.accounts',
    'src.wsite',
    'src.zoom_api',

    'src.portals.moderator',
    'src.portals.parent',
    'src.portals.student',
    'src.portals.admins',

    # MUST BE AT THE END
    'notifications'
]

""" SECURITY AND MIDDLEWARES -------------------------------------------------------------------------------------"""

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'preventconcurrentlogins.middleware.PreventConcurrentLoginsMiddleware'
]

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', },
]

""" TEMPLATES AND DATABASES -------------------------------------------------------------------------------------- """
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

if SERVER:
    if os.name == 'posix':
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.mysql',
                'OPTIONS': {'charset': 'utf8mb4'},
                'NAME': 'cocognitodb',
                'USER': 'umair',
                'PASSWORD': 'multi-mediaplus123',
                'HOST': 'localhost',
                'PORT': '3306',
            }
        }
    elif os.name == 'nt':
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.mysql',
                'OPTIONS': {'charset': 'utf8mb4'},
                'NAME': 'cocognitodb',
                'USER': 'umair_windows',
                'PASSWORD': 'multi-mediaplus123',
                'HOST': '139.59.45.36',
                'PORT': '3306',
            }
        }
else:
    if USE_TESTING_DB_SERVER:
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': os.path.join(BASE_DIR, 'db_unchanged.sqlite3'),
            }
        }
    else:
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
            }
        }

""" INTERNATIONALIZATION ----------------------------------------------------------------------------------------- """

LANGUAGE_CODE = 'en-us'
if TEST:
    TIME_ZONE = 'Asia/Tashkent'
else:
    TIME_ZONE = 'Asia/Calcutta'
USE_I18N = True
USE_L10N = True
USE_TZ = True

""" PATHS STATIC AND MEDIA --------------------------------------------------------------------------------------- """

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]
STATIC_ROOT = os.path.join(BASE_DIR, 'assets')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

""" EMAIL AND ALL AUTH ------------------------------------------------------------------------------------------- """

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'donald.duck0762@gmail.com'
EMAIL_HOST_PASSWORD = 'ugtykpnhepxvchqz'
EMAIL_PORT = 587
DEFAULT_FROM_EMAIL = 'COCOGNITO-Team <noreply@application.com>'

SOCIALACCOUNT_PROVIDERS = {
    'google': {'SCOPE': ['profile', 'email', ],
               'AUTH_PARAMS': {'access_type': 'online', }}
}

ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
OLD_PASSWORD_FIELD_ENABLED = True
LOGOUT_ON_PASSWORD_CHANGE = False
ACCOUNT_EMAIL_VERIFICATION = 'none'

""" RESIZER IMAGE --------------------------------------------------------------------------------"""
DJANGORESIZED_DEFAULT_SIZE = [1920, 1080]
DJANGORESIZED_DEFAULT_QUALITY = 75
DJANGORESIZED_DEFAULT_KEEP_META = True
DJANGORESIZED_DEFAULT_FORCE_FORMAT = 'JPEG'
DJANGORESIZED_DEFAULT_FORMAT_EXTENSIONS = {
    'JPEG': ".jpg",
    'PNG': ".png",
    'GIF': ".gif"
}
DJANGORESIZED_DEFAULT_NORMALIZE_ROTATION = True
