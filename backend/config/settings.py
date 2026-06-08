"""
Django settings for Porsuk: Sınav Koçu project.
"""

import os
from pathlib import Path
from decouple import config, Csv
from django.templatetags.static import static
from django.urls import reverse_lazy

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY
SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1', cast=Csv())

# Application definition
INSTALLED_APPS = [
    # Unfold must be before django.contrib.admin
    'unfold',
    'unfold.contrib.filters',
    'unfold.contrib.forms',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party
    'rest_framework',
    'corsheaders',

    # Local apps
    'core',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
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
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Database — PostgreSQL (production) / SQLite (local dev)
USE_SQLITE = config('USE_SQLITE', default=False, cast=bool)

if USE_SQLITE:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': config('DB_NAME', default='porsuk_db'),
            'USER': config('DB_USER', default='porsuk_user'),
            'PASSWORD': config('DB_PASSWORD', default='porsuk_pass'),
            'HOST': config('DB_HOST', default='db'),
            'PORT': config('DB_PORT', default='5432'),
        }
    }

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization — Turkish
LANGUAGE_CODE = 'tr'
TIME_ZONE = 'Europe/Istanbul'
USE_I18N = True
USE_TZ = True

# Static & Media files
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# CORS — Allow mobile app to connect
CORS_ALLOW_ALL_ORIGINS = True  # Tighten in production

# DRF Settings
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
}

# ──────────────────────────────────────────────
# UNFOLD SETTINGS — Modern & Professional Admin
# ──────────────────────────────────────────────
UNFOLD = {
    "SITE_TITLE": "Porsuk: Sınav Koçu",
    "SITE_HEADER": "Porsuk",
    "SITE_SUBHEADER": "Sınav Koçu Yönetim Paneli",
    "SITE_DROPDOWN": [
        {
            "icon": "api",
            "title": "API Tarayıcı",
            "link": "/api/",
        },
    ],
    "SITE_URL": "/",
    "SHOW_HISTORY": True,
    "SHOW_VIEW_ON_SITE": False,

    # Sidebar navigation
    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": False,
        "navigation": [
            {
                "title": "Genel",
                "separator": True,
                "collapsible": False,
                "items": [
                    {
                        "title": "Anasayfa",
                        "icon": "dashboard",
                        "link": reverse_lazy("admin:index"),
                    },
                ],
            },
            {
                "title": "İçerik Yönetimi",
                "separator": True,
                "collapsible": False,
                "items": [
                    {
                        "title": "Sınav Tarihleri",
                        "icon": "event",
                        "link": reverse_lazy("admin:core_examdate_changelist"),
                        "badge": "core.utils.exam_date_badge",
                    },
                    {
                        "title": "Günün Soruları",
                        "icon": "quiz",
                        "link": reverse_lazy("admin:core_dailyquestion_changelist"),
                    },
                    {
                        "title": "Teşhis Testleri",
                        "icon": "biotech",
                        "link": reverse_lazy("admin:core_diagnostictest_changelist"),
                    },
                    {
                        "title": "Duyurular",
                        "icon": "campaign",
                        "link": reverse_lazy("admin:core_announcement_changelist"),
                    },
                    {
                        "title": "Motivasyon Sözleri",
                        "icon": "format_quote",
                        "link": reverse_lazy("admin:core_motivationalquote_changelist"),
                    },
                    {
                        "title": "Formül Kartları",
                        "icon": "functions",
                        "link": reverse_lazy("admin:core_formulacard_changelist"),
                    },
                ],
            },
            {
                "title": "Bildirimler",
                "separator": True,
                "collapsible": False,
                "items": [
                    {
                        "title": "Push Bildirimler",
                        "icon": "notifications_active",
                        "link": reverse_lazy("admin:core_notification_changelist"),
                        "badge": "core.utils.unsent_notifications_badge",
                    },
                    {
                        "title": "Cihaz Token'ları",
                        "icon": "devices",
                        "link": reverse_lazy("admin:core_devicetoken_changelist"),
                        "badge": "core.utils.device_count_badge",
                    },
                ],
            },
            {
                "title": "CRM",
                "separator": True,
                "collapsible": False,
                "items": [
                    {
                        "title": "Potansiyel Öğrenciler",
                        "icon": "contacts",
                        "link": reverse_lazy("admin:core_leadcontact_changelist"),
                        "badge": "core.utils.new_leads_badge",
                    },
                ],
            },
            {
                "title": "Ayarlar & Sistem",
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": "Uygulama Ayarları",
                        "icon": "settings",
                        "link": reverse_lazy("admin:core_appsettings_changelist"),
                    },
                    {
                        "title": "Kullanıcılar",
                        "icon": "person",
                        "link": reverse_lazy("admin:auth_user_changelist"),
                    },
                    {
                        "title": "Gruplar",
                        "icon": "group",
                        "link": reverse_lazy("admin:auth_group_changelist"),
                    },
                ],
            },
        ],
    },

    # Theme colors — custom primary color (indigo/purple accent)
    "COLORS": {
        "primary": {
            "50": "238 242 255",
            "100": "224 231 255",
            "200": "199 210 254",
            "300": "165 180 252",
            "400": "129 140 248",
            "500": "99 102 241",
            "600": "79 70 229",
            "700": "67 56 202",
            "800": "55 48 163",
            "900": "49 46 129",
            "950": "30 27 75",
        },
    },

    # Tabs for dashboard
    "TABS": [
        {
            "models": ["core.examdate"],
            "items": [
                {
                    "title": "Sınav Tarihleri",
                    "link": reverse_lazy("admin:core_examdate_changelist"),
                },
            ],
        },
    ],
}
