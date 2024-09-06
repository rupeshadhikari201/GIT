from pathlib import Path
from datetime import timedelta
import os

# Import dj-database-url at the beginning of the file.
import dj_database_url

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

BASE_URL = 'http://localhost:8000' if os.getenv('PRODUCTION') == 'False' else 'https://gokap.onrender.com'

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-%5q47umd@xh^prb1sx8mciadquxqg64-76d1&+z=8#w$shw#h4"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    
    # my apps
    "register",
    "freelancer", 
    "client",
    "project",
    "payment",
    "common",
    
    "rest_framework",
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'corsheaders',
    
    # dbbackup
    'dbbackup',
    
    # swagger
    'drf_yasg',
    'rest_framework_swagger',
    
    # django extensions
    
]
# say django to use account.user as the default user
AUTH_USER_MODEL = "register.User"

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    
    # whitenoise middleware
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

# "*"  # Allow all origins (not recommended for production)
# CORS_ALLOWED_ORIGINS = [
#     "https://rupeshadhikari201.github.io",  
#     "http://localhost:5173",
#     "http://localhost:8000",
#     "http://127.0.0.1:8000",
# ]
CORS_ALLOW_ALL_ORIGINS = True

# Rest Framework
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        # 'rest_framework.renderers.BrowsableAPIRenderer',
    ], 
    
    # JWT Authentication
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),
}
SWAGGER_SETTINGS = {
   'USE_SESSION_AUTH': False
}

ROOT_URLCONF = "backend.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR,'templates')],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "backend.wsgi.application"

database_url = os.getenv('DATABASE_URL')
DATABASES = {
    # "default": {
    #     "ENGINE": "django.db.backends.postgresql",
    #     "NAME": "postgres1",
    #     "USER": "postgres",
    #     "HOST": "localhost",
    #     "PORT": '5432',
    #     "PASSWORD": 12345
    # },
  
    # 'default': {
    # 'ENGINE': 'django.db.backends.postgresql',
    # 'NAME': os.getenv('PGDATABASE'),
    # 'USER': os.getenv('PGUSER'),
    # 'PASSWORD': os.getenv('PGPASSWORD'),
    # 'HOST': os.getenv('PGHOST'),
    # 'PORT': os.getenv('PGPORT', 5432),
    # 'OPTIONS': {
    #   'sslmode': 'require',
    # },
    # },
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL'),
        conn_max_age=600,
        conn_health_checks=True,
        # ssl_require=True,
    )
}

EMAIL_BACKEND = os.getenv("EMAIL_BACKEND")
EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS")
EMAIL_PORT = os.getenv("EMAIL_PORT")
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")

# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587
# EMAIL_HOST_USER = '21bcs11201@gmail.com'
# EMAIL_HOST_PASSWORD = 'uoba zdxf aucb uxih'


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",},
]


# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
print("base dir " , BASE_DIR)
print("base url " , BASE_URL)
STATIC_URL  = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')        

# Static File Storeage Backend
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage' 


# Media Files (Uploads)
MEDIA_URL  = '/media/'                          # This is the URL that will be used to access media files in the browser. ex it can be accessed at http://your-domain.com/media/filename.jpg.
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')    # This is the absolute filesystem path to the directory where media files will be stored.
''' MEDIA_URL and MEDIA_ROOT are settings in settings.py that define where media files will be stored and how they will be accessed.'''


# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Simple JWT
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=20),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": False,
    "UPDATE_LAST_LOGIN": False,

    "ALGORITHM": "HS256",
    # "SIGNING_KEY": settings.SECRET_KEY,
    "VERIFYING_KEY": "",
    "AUDIENCE": None,
    "ISSUER": None,
    "JSON_ENCODER": None,
    "JWK_URL": None,
    "LEEWAY": 0,

    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",

    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",

    "JTI_CLAIM": "jti",

    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=60),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),

    "TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainPairSerializer",
    "TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSerializer",
    "TOKEN_VERIFY_SERIALIZER": "rest_framework_simplejwt.serializers.TokenVerifySerializer",
    "TOKEN_BLACKLIST_SERIALIZER": "rest_framework_simplejwt.serializers.TokenBlacklistSerializer",
    "SLIDING_TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainSlidingSerializer",
    "SLIDING_TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSlidingSerializer",
}

# DBBACKUP library configurations
DBBACKUP_STORAGE = 'django.core.files.storage.FileSystemStorage'
DBBACKUP_STORAGE_OPTIONS = {'location': BASE_DIR / 'dbbackup'}
# Use the --no-owner and --no-acl options:
# These options tell pg_restore to skip ownership and access control commands. Modify your Django settings to include these options:
DBBACKUP_POSTGRES_RESTORE_EXTRA_ARGS = ['--no-owner', '--no-acl']
# hey, when you are unable to restore the database run this command 
# pg_restore --dbname=postgresql://gokap-database_owner:4fRbNwksu3Va@ep-fragrant-darkness-a1vcs7w6.ap-southeast-1.aws.neon.tech/gokap-database --single-transaction --clean --no-owner --no-acl path/to/your/backup/file(full path)
print(DBBACKUP_STORAGE_OPTIONS['location'])
