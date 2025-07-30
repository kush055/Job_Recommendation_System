import os
from pathlib import Path
from django.contrib.messages import constants as messages

# === Base Paths ===
BASE_DIR = Path(__file__).resolve().parent.parent

# === Security ===
SECRET_KEY = 'your-secret-key-here'  # Replace this with a secure value in production!
DEBUG = True
ALLOWED_HOSTS = []

# === Installed Apps ===
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'widget_tweaks',             # For form styling in templates
    'django.contrib.humanize',   # For formatting numbers, times, etc.

    # Local apps
    'resumes',
    'accounts',
    'jobs',
]

# === Middleware ===
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# === URL Configuration ===
ROOT_URLCONF = 'job_recommendation.urls'

# === Templates ===
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Global templates folder
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

# === WSGI ===
WSGI_APPLICATION = 'job_recommendation.wsgi.application'

# === Database (PostgreSQL) ===
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'db_backup',
        'USER': 'postgres',
        'PASSWORD': 'Xzetsu0528',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# === Password Validation ===
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# === Localization ===
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# === Static Files ===
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']        # For dev server
STATIC_ROOT = BASE_DIR / 'staticfiles'          # For collectstatic in production

# === Media Files ===
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# === Default Primary Key Field Type ===
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# === Authentication Redirects ===
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/resumes/upload/'
LOGOUT_REDIRECT_URL = '/accounts/login/'

# === Django Messages → Bootstrap Classes ===
MESSAGE_TAGS = {
    messages.ERROR: 'danger',
    messages.SUCCESS: 'success',
}

# === Session Configuration (Auto logout after inactivity) ===
SESSION_COOKIE_AGE = 900  # 15 minutes
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_SAVE_EVERY_REQUEST = True

# === Encryption Keys ===
KEYS_DIR = BASE_DIR / 'keys'
PRIVATE_KEY_PATH = KEYS_DIR / 'private_key.pem'
PUBLIC_KEY_PATH = KEYS_DIR / 'public_key.pem'

# Ensure the keys directory exists
os.makedirs(KEYS_DIR, exist_ok=True)