from pathlib import Path
import sys
from urllib.parse import urlparse, urlunparse
import environ

BASE_DIR = Path(__file__).resolve().parent.parent
PROJECT_DIR = BASE_DIR.parent

env = environ.Env(
    DEBUG=(bool, False)
)

# Lokal sozlamalar backend ichida ham, loyiha rootida ham turishi mumkin.
for env_file in (PROJECT_DIR / '.env', BASE_DIR / '.env'):
    if env_file.exists():
        environ.Env.read_env(env_file)


def _is_running_in_docker() -> bool:
    return Path('/.dockerenv').exists() or env.bool('RUNNING_IN_DOCKER', default=False)


IS_LOCAL_RUNSERVER = not _is_running_in_docker() and 'runserver' in sys.argv


def _resolve_service_host(host: str, *, local_port: str | None = None) -> tuple[str, str | None]:
    if _is_running_in_docker():
        return host, None

    docker_service_ports = {
        'db': local_port or '5433',
        'redis': local_port or '6379',
    }
    if host in docker_service_ports:
        return '127.0.0.1', docker_service_ports[host]

    return host, None


def _resolve_redis_location(location: str) -> str:
    parsed = urlparse(location)
    hostname = parsed.hostname
    if not hostname:
        return location

    resolved_host, resolved_port = _resolve_service_host(hostname, local_port='6379')
    if resolved_host == hostname and resolved_port is None:
        return location

    netloc = resolved_host
    if parsed.username:
        netloc = parsed.username
        if parsed.password:
            netloc = f'{netloc}:{parsed.password}'
        netloc = f'{netloc}@{resolved_host}'
    if resolved_port or parsed.port:
        netloc = f'{netloc}:{resolved_port or parsed.port}'

    return urlunparse(parsed._replace(netloc=netloc))

SECRET_KEY = env('SECRET_KEY')

DEBUG = env('DEBUG') or IS_LOCAL_RUNSERVER

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['localhost', '127.0.0.1'])
for local_host in ('localhost', '127.0.0.1'):
    if local_host not in ALLOWED_HOSTS:
        ALLOWED_HOSTS.append(local_host)

SECURE_SSL_REDIRECT = env.bool('SECURE_SSL_REDIRECT', default=not DEBUG and not IS_LOCAL_RUNSERVER)
SESSION_COOKIE_SECURE = env.bool('SESSION_COOKIE_SECURE', default=not DEBUG and not IS_LOCAL_RUNSERVER)
CSRF_COOKIE_SECURE = env.bool('CSRF_COOKIE_SECURE', default=not DEBUG and not IS_LOCAL_RUNSERVER)
SECURE_HSTS_SECONDS = env.int('SECURE_HSTS_SECONDS', default=31536000 if not DEBUG and not IS_LOCAL_RUNSERVER else 0)
SECURE_HSTS_INCLUDE_SUBDOMAINS = env.bool('SECURE_HSTS_INCLUDE_SUBDOMAINS', default=not DEBUG and not IS_LOCAL_RUNSERVER)
SECURE_HSTS_PRELOAD = env.bool('SECURE_HSTS_PRELOAD', default=not DEBUG and not IS_LOCAL_RUNSERVER)


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
DB_HOST = env('DB_HOST', default='localhost')
DB_PORT = env('DB_PORT', default='5432')
DB_HOST, fallback_db_port = _resolve_service_host(DB_HOST, local_port='5433')
if fallback_db_port and DB_PORT == '5432':
    DB_PORT = fallback_db_port

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': DB_HOST,
        'PORT': DB_PORT,
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
STATIC_URL = env('STATIC_URL', default='/static/')
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = env('MEDIA_URL', default='/media/')
MEDIA_ROOT = BASE_DIR / 'media'


# Cache — Redis in containers/production, in-memory cache for local runserver.
REDIS_URL = _resolve_redis_location(env('REDIS_URL', default='redis://127.0.0.1:6379/1'))

if IS_LOCAL_RUNSERVER:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            'LOCATION': 'sinax-local-dev',
        }
    }
else:
    CACHES = {
        'default': {
            'BACKEND': 'django_redis.cache.RedisCache',
            'LOCATION': REDIS_URL,
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
for local_origin in ('http://localhost:3000', 'http://127.0.0.1:3000', 'http://localhost:5173', 'http://127.0.0.1:5173'):
    if local_origin not in CORS_ALLOWED_ORIGINS:
        CORS_ALLOWED_ORIGINS.append(local_origin)

CSRF_TRUSTED_ORIGINS = env.list('CSRF_TRUSTED_ORIGINS', default=[])
for local_origin in ('http://localhost:3000', 'http://127.0.0.1:3000', 'http://localhost:5173', 'http://127.0.0.1:5173'):
    if local_origin not in CSRF_TRUSTED_ORIGINS:
        CSRF_TRUSTED_ORIGINS.append(local_origin)


# Telegram bot
BOT_TOKEN = env('BOT_TOKEN', default='')
TELEGRAM_GROUP_ID = env('TELEGRAM_GROUP_ID', default='')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
