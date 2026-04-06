from pathlib import Path
import environ

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env(
    DEBUG=(bool, True)
)

# Faqat .env fayl mavjud bo'lsa o'qi (lokal uchun)
env_file = BASE_DIR / '.env'
if env_file.exists():
    environ.Env.read_env(env_file)

SECRET_KEY = env('SECRET_KEY', default='django-insecure-3bc00!&(l!sbyv=5)e4$!=ta$z^vx@q(ci=$j65aje!=e63d5u')

DEBUG = env('DEBUG')

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['*'])


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third party
    'rest_framework',
    'drf_spectacular',
    'corsheaders',

    # My apps
    'apps.core',
    'apps.applications',
    'apps.certificates',
    'apps.gallery',
    'apps.partners',
    'apps.products',
    'apps.services',
    'apps.specialists',
    'apps.testimonials',
    'apps.faq',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',          # CORS — CommonMiddleware dan oldin
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': env('DB_HOST', default='localhost'),
        'PORT': env('DB_PORT', default='5432'),
    }
}


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Tashkent'
USE_I18N = True
USE_TZ = True


# Static & Media
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# Cache — Redis
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': env('REDIS_URL', default='redis://127.0.0.1:6379/1'),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}


# REST Framework
REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}


# drf-spectacular
SPECTACULAR_SETTINGS = {
    'TITLE': 'TZZ API',
    'DESCRIPTION': 'Masketniy setka, Jalyuzi, Dushovoy Kabinka va Remont Okon xizmatlari API',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
}


# CORS
CORS_ALLOWED_ORIGINS = env.list('CORS_ALLOWED_ORIGINS', default=[
    'http://localhost:3000',
    'http://localhost:5173',
])


# Telegram bot
BOT_TOKEN = env('BOT_TOKEN', default='')
TELEGRAM_GROUP_ID = env('TELEGRAM_GROUP_ID', default='')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'