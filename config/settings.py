"""
config/settings.py

TagsBikez — Django 5 project settings.
Environment variables are loaded from .env via python-decouple.
Copy .env.example → .env and fill in your values before running.
"""

import os
from pathlib import Path
from decouple import config, Csv

# ─────────────────────────────────────────────────────────────────────────────
# PATHS
# ─────────────────────────────────────────────────────────────────────────────

BASE_DIR = Path(__file__).resolve().parent.parent


# ─────────────────────────────────────────────────────────────────────────────
# SECURITY
# ─────────────────────────────────────────────────────────────────────────────

SECRET_KEY = config('SECRET_KEY', default='django-insecure-change-me-before-production')

DEBUG = config('DEBUG', default=True, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='127.0.0.1,localhost', cast=Csv())


# ─────────────────────────────────────────────────────────────────────────────
# INSTALLED APPS
# ─────────────────────────────────────────────────────────────────────────────

INSTALLED_APPS = [

    "jazzmin",
    # Django core
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party
    'rest_framework',
    'django_filters',
    'corsheaders',

    # Project apps
    'apps.home',
    'apps.events',
    'apps.gallery',
    'apps.categories',
    'apps.motorcycles',
    'apps.api',
    'apps.careers', 
]


# ─────────────────────────────────────────────────────────────────────────────
# MIDDLEWARE
# ─────────────────────────────────────────────────────────────────────────────

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',          # must be first
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# ─────────────────────────────────────────────────────────────────────────────
# URLS & WSGI
# ─────────────────────────────────────────────────────────────────────────────

ROOT_URLCONF = 'config.urls'
WSGI_APPLICATION = 'config.wsgi.application'
ASGI_APPLICATION = 'config.asgi.application'


# ─────────────────────────────────────────────────────────────────────────────
# TEMPLATES
# ─────────────────────────────────────────────────────────────────────────────

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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


# ─────────────────────────────────────────────────────────────────────────────
# DATABASE
# ─────────────────────────────────────────────────────────────────────────────

_db_engine = config('DB_ENGINE', default='django.db.backends.sqlite3')

if _db_engine == 'django.db.backends.sqlite3':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE':   _db_engine,
            'NAME':     config('DB_NAME'),
            'USER':     config('DB_USER'),
            'PASSWORD': config('DB_PASSWORD'),
            'HOST':     config('DB_HOST', default='localhost'),
            'PORT':     config('DB_PORT', default='5432'),
        }
    }


# ─────────────────────────────────────────────────────────────────────────────
# PASSWORD VALIDATION
# ─────────────────────────────────────────────────────────────────────────────

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# ─────────────────────────────────────────────────────────────────────────────
# INTERNATIONALISATION
# ─────────────────────────────────────────────────────────────────────────────

LANGUAGE_CODE = 'en-us'
TIME_ZONE     = 'Asia/Kolkata'
USE_I18N      = True
USE_TZ        = True


# ─────────────────────────────────────────────────────────────────────────────
# STATIC & MEDIA FILES
# ─────────────────────────────────────────────────────────────────────────────

STATIC_URL  = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static'] if (BASE_DIR / 'static').exists() else []

MEDIA_URL  = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# ─────────────────────────────────────────────────────────────────────────────
# DEFAULT PRIMARY KEY
# ─────────────────────────────────────────────────────────────────────────────

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ─────────────────────────────────────────────────────────────────────────────
# DJANGO REST FRAMEWORK
# ─────────────────────────────────────────────────────────────────────────────

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.MultiPartParser',
        'rest_framework.parsers.FormParser',
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.OrderingFilter',
        'rest_framework.filters.SearchFilter',
    ],
    'DEFAULT_PAGINATION_CLASS': 'apps.api.pagination.StandardResultsPagination',
    'PAGE_SIZE': 12,
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'EXCEPTION_HANDLER': 'apps.api.exceptions.custom_exception_handler',
}


# ─────────────────────────────────────────────────────────────────────────────
# CORS  (django-cors-headers)
# ─────────────────────────────────────────────────────────────────────────────

CORS_ALLOWED_ORIGINS = config(
    'CORS_ALLOWED_ORIGINS',
    default='http://localhost:3000,http://localhost:5173',
    cast=Csv(),
)

CORS_ALLOW_ALL_ORIGINS = DEBUG   # handy during local dev; tighten for production

CORS_ALLOW_METHODS = [
    'DELETE', 'GET', 'OPTIONS', 'PATCH', 'POST', 'PUT',
]

CORS_ALLOW_HEADERS = [
    'accept', 'accept-encoding', 'authorization',
    'content-type', 'dnt', 'origin',
    'user-agent', 'x-csrftoken', 'x-requested-with',
]

# -------------------------------------------------------

# ─────────────────────────────────────────────
# JAZZMIN — Admin UI Customization
# Theme: Black sidebar, Red accents, White content
# ─────────────────────────────────────────────
JAZZMIN_SETTINGS = {
    # ── Branding ──────────────────────────────
    "site_title": "TagsBikez Admin",
    "site_header": "TagsBikez",
    "site_brand": "TagsBikez",
    "site_logo": "tagsbikezwhitelogo.png",
    "site_logo_classes": "img-circle",
    "login_logo": "tag7slogo-small.png",
    "login_logo_dark": "tagsbikezwhitelogo.webp",
    "site_icon": "tagsbikezwhitelogo.webp",
    "welcome_sign": "Welcome to TagsBikez Admin",
    "copyright": "TagsBikez © 2025",

    # ── Search ────────────────────────────────
    "search_model": ["auth.user"],
    "user_avatar": None,

    # ── Top Navigation ────────────────────────
    "topmenu_links": [
        {"name": "Home", "url": "admin:index", "permissions": ["auth.view_user"]},
        {"name": "View API", "url": "/api/", "new_window": True},
        {"model": "auth.User"},
    ],

    # ── User Menu ─────────────────────────────
    "usermenu_links": [
        {"model": "auth.user"},
    ],

    # ── Sidebar ───────────────────────────────
    "show_sidebar": True,
    "navigation_expanded": True,
    "hide_apps": [],
    "hide_models": [],

    # Custom sidebar order
    "order_with_respect_to": [
        "categories",
        "categories.ProductCategory",
        "categories.ProductCategoryAbout",
        "categories.ProductCategoryBottomSection",
        "motorcycles",
        "motorcycles.MotorcycleProduct",
        "motorcycles.ProductFeatureSection",
        "about",
        "about.AboutPage",
        "about.LeadershipMember",
        "about.AboutGallery",
        "auth",
    ],

    # ── Sidebar Icons ─────────────────────────
    "icons": {
        "auth":                                    "fas fa-users-cog",
        "auth.user":                               "fas fa-user",
        "auth.Group":                              "fas fa-users",
        "categories.ProductCategory":              "fas fa-tags",
        "categories.ProductCategoryAbout":         "fas fa-info-circle",
        "categories.ProductCategoryBottomSection": "fas fa-layer-group",
        "motorcycles.MotorcycleProduct":           "fas fa-motorcycle",
        "motorcycles.ProductFeatureSection":       "fas fa-star",
        "about.AboutPage":                         "fas fa-file-alt",
        "about.LeadershipMember":                  "fas fa-user-tie",
        "about.AboutGallery":                      "fas fa-images",
    },
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",

    # ── Related Modal ─────────────────────────
    "related_modal_active": True,

    # ── UI Tweaks ─────────────────────────────
    # "custom_css": "admin/css/tagsbikez_admin.css",   # ✅ FIXED — correct location
    # "custom_js": None,
    # "use_google_fonts_cdn": True,
    # "show_ui_builder": False,

    # ── Change View ───────────────────────────
    "changeform_format": "horizontal_tabs",
}

# JAZZMIN_UI_TWEAKS = {
#     "navbar_small_text": False,
#     "footer_small_text": False,
#     "body_small_text": False,
#     "brand_small_text": False,

#     # Red accent color throughout
#     "accent": "accent-danger",

#     # Top navbar — BLACK background stays
#     "navbar": "navbar-dark navbar-danger",
#     "no_navbar_border": True,

#     # Sidebar — BLACK with red active highlight stays
#     "sidebar": "sidebar-dark-danger",
#     "sidebar_nav_small_text": False,
#     "sidebar_disable_expand": False,
#     "sidebar_nav_child_indent": True,
#     "sidebar_nav_compact_style": False,
#     "sidebar_nav_legacy_style": False,
#     "sidebar_nav_flat_style": False,

#     # ✅ CHANGED: light theme so content area is white
#     "theme": "flatly",          # was "darkly" — this was forcing dark bg on all inputs

#     # Sticky action buttons at top
#     "actions_sticky_top": True,

#     # All primary buttons → red
#     "button_classes": {
#         "primary":   "btn-danger",
#         "secondary": "btn-outline-secondary",
#         "info":      "btn-outline-info",
#         "warning":   "btn-warning",
#         "danger":    "btn-danger",
#         "success":   "btn-success",
#     },
# }