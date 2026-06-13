import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'your-default-secret-key')
DEBUG = os.environ.get('DEBUG', 'False') == 'False'

ALLOWED_HOSTS = os.environ.get(
    'ALLOWED_HOSTS',
    'www.kiliacore.com,localhost,127.0.0.1'
).split(',')

# Application definition
INSTALLED_APPS = [
    'django.contrib.staticfiles',   # only if you serve static files
    'kiliacore',                    # your landing page app
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

ROOT_URLCONF = 'config.urls'
CSRF_TRUSTED_ORIGINS = [
    'https://www.kiliacore.com',
    'https://kiliacore.com',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],                 # or add a global templates dir if needed
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.static',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Database – none needed unless you later store contact form data
# For zero‑DB setup, use the dummy backend:
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

# Static files (if your landing page uses CSS/JS/images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Email settings for the contact form
if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    # Use Resend HTTP API (no SMTP)
    EMAIL_BACKEND = 'core.email_backends.ResendHTTPBackend'

RESEND_API_KEY = os.environ.get('RESEND_API_KEY')   # must be set

DEFAULT_FROM_EMAIL = 'support@kiliacore.com'
SERVER_EMAIL = 'support@kiliacore.com'
SUPPORT_EMAIL = 'kiliacoresoftware@gmail.com'