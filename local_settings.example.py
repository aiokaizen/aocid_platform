# Copy to local_settings.py (gitignored; holds secrets). Imported at the end of settings.py.

# --- Database (PostgreSQL) ---
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "aocid_db",
        "USER": "aocid_db_user",
        "PASSWORD": "CHANGE_ME",
        "HOST": "db",       # 'db' under docker-compose; overridable via DB_HOST env
        "PORT": "5432",     # overridable via DB_PORT env
    }
}

# --- Security / reverse proxy ---
DEBUG = False
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
ALLOWED_HOSTS = ["aitourirchessclub.ma", "www.aitourirchessclub.ma", "localhost", "127.0.0.1"]
CSRF_TRUSTED_ORIGINS = ["https://aitourirchessclub.ma", "https://www.aitourirchessclub.ma"]

# --- Email (self-hosted SMTP via mail.sentinel.ma) ---
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "mail.sentinel.ma"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_HOST_USER = "noreply@aitourirchessclub.ma"
EMAIL_HOST_PASSWORD = "CHANGE_ME"
DEFAULT_FROM_EMAIL = "noreply@aitourirchessclub.ma"
SERVER_EMAIL = "noreply@aitourirchessclub.ma"
