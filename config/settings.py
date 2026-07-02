"""
Configurações do projeto Metalab Web Django MVP.

Variáveis de ambiente (via python-decouple, arquivo .env):
    SECRET_KEY            — obrigatória em produção
    DEBUG                 — True local, False em produção
    ALLOWED_HOSTS         — hosts separados por vírgula
    DATABASE_URL          — PostgreSQL em produção; vazio usa SQLite local
    CSRF_TRUSTED_ORIGINS  — origens https separadas por vírgula
"""

from pathlib import Path

import dj_database_url
from django.core.exceptions import ImproperlyConfigured
from decouple import Csv, config

BASE_DIR = Path(__file__).resolve().parent.parent

# ─── Segurança ───────────────────────────────────────────────────────────────

DEBUG = config("DEBUG", default=True, cast=bool)
SECRET_KEY = config("SECRET_KEY", default="dev-only-insecure-key-change-me" if DEBUG else "")
ALLOWED_HOSTS = config("ALLOWED_HOSTS", default="localhost,127.0.0.1", cast=Csv())
CSRF_TRUSTED_ORIGINS = config("CSRF_TRUSTED_ORIGINS", default="", cast=Csv())

if not DEBUG and (
    not SECRET_KEY
    or SECRET_KEY in {"dev-only-insecure-key-change-me", "change-me"}
    or len(SECRET_KEY) < 50
):
    raise ImproperlyConfigured("Defina uma SECRET_KEY forte antes de rodar em producao.")

if not DEBUG:
    SECURE_SSL_REDIRECT = config("SECURE_SSL_REDIRECT", default=True, cast=bool)
    SESSION_COOKIE_SECURE = config("SESSION_COOKIE_SECURE", default=True, cast=bool)
    CSRF_COOKIE_SECURE = config("CSRF_COOKIE_SECURE", default=True, cast=bool)
    SECURE_HSTS_SECONDS = config("SECURE_HSTS_SECONDS", default=3600, cast=int)
    SECURE_HSTS_INCLUDE_SUBDOMAINS = config(
        "SECURE_HSTS_INCLUDE_SUBDOMAINS", default=False, cast=bool
    )
    SECURE_HSTS_PRELOAD = config("SECURE_HSTS_PRELOAD", default=False, cast=bool)
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# ─── Apps ────────────────────────────────────────────────────────────────────

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    # Apps do projeto
    "core",
    "accounts",
    "produtos",
    "clientes",
    "pedidos",
    "cupons",
    "banners",
    "checkout",
    "relatorios",
    "api",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "core.middleware.LoginRateLimitMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "core.middleware.SecurityHeadersMiddleware",
]

ROOT_URLCONF = "config.urls"
CSRF_FAILURE_VIEW = "core.views.csrf_failure"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "core.context_processors.loja",
                "checkout.context_processors.carrinho",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# ─── Banco de dados ──────────────────────────────────────────────────────────
# SQLite local por padrão; PostgreSQL em produção via DATABASE_URL.

DATABASE_URL = config("DATABASE_URL", default="")
if not DEBUG and not DATABASE_URL:
    raise ImproperlyConfigured("Defina DATABASE_URL em producao.")

DATABASES = {
    "default": (
        dj_database_url.parse(DATABASE_URL, conn_max_age=600)
        if DATABASE_URL
        else dj_database_url.parse(f"sqlite:///{BASE_DIR / 'db.sqlite3'}", conn_max_age=600)
    )
}

# ─── Autenticação ────────────────────────────────────────────────────────────

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LOGIN_URL = "accounts:login"
LOGIN_REDIRECT_URL = "core:home"
LOGOUT_REDIRECT_URL = "core:home"

# ─── Internacionalização ─────────────────────────────────────────────────────

LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Sao_Paulo"
USE_I18N = True
USE_TZ = True

# ─── Estáticos e mídia ───────────────────────────────────────────────────────

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
# Manifest (hash nos nomes) só em produção; em dev/testes usa o storage simples.
STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {
        "BACKEND": (
            "django.contrib.staticfiles.storage.StaticFilesStorage"
            if DEBUG
            else "whitenoise.storage.CompressedManifestStaticFilesStorage"
        )
    },
}

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ─── Hardening ───────────────────────────────────────────────────────────────

MAX_IMAGE_UPLOAD_SIZE = config("MAX_IMAGE_UPLOAD_SIZE", default=5 * 1024 * 1024, cast=int)
RATE_LIMIT_LOGIN_ATTEMPTS = config("RATE_LIMIT_LOGIN_ATTEMPTS", default=8, cast=int)
RATE_LIMIT_LOGIN_WINDOW = config("RATE_LIMIT_LOGIN_WINDOW", default=300, cast=int)
RATE_LIMIT_LOGIN_PATHS = {"/login/", "/django-admin/login/"}
HEALTHCHECK_INCLUDE_DATABASE = config("HEALTHCHECK_INCLUDE_DATABASE", default=False, cast=bool)

# ─── Loja ────────────────────────────────────────────────────────────────────

LOJA_NOME = config("LOJA_NOME", default="Metalab")
# Frete fixo simples até integrar Melhor Envio; frete grátis acima do limite.
FRETE_FIXO = config("FRETE_FIXO", default="19.90")
FRETE_GRATIS_ACIMA_DE = config("FRETE_GRATIS_ACIMA_DE", default="199.00")
