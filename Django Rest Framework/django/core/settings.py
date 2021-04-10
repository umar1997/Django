from pathlib import Path
from datetime import timedelta
import os

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'apuvicmef^(!j8gx&clu0u(!8m0r^etok^l0)kc!---#(i5=dt'
DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'rest_framework',
    'django.contrib.admin',
    'django.contrib.auth',
    # These are contrib,admin dependencies used in blog/admin
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    # JWT Auth
    'rest_framework_simplejwt.token_blacklist',
    ##############################################
    'django.contrib.staticfiles',
    'blog',
    'blog_api',
    'corsheaders',
    'users',
    # Oauth
    'oauth2_provider',
    'social_django',
    'drf_social_oauth2',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # Oauth
    # 'social_django.middleware.SocialAuthExceptionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',

    # FOR /admin/ page
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    #################
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                # FOR /admin/ page
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # Oauth
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]

CORS_ALLOW_ALL_ORIGINS = True

# CHECK THIS OUT: https://www.django-rest-framework.org/api-guide/permissions/
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        # 'rest_framework.permissions.IsAuthenticated', IsAdminUser, IsAuthenticatedOrReadOnly (Authenticated can update, Anons can read)
        'rest_framework.permissions.AllowAny',
    ],
    # To disable authentication comment this class
    # 'DEFAULT_AUTHENTICATION_CLASSES': (

            # JWT
    #     # https://django-rest-framework-simplejwt.readthedocs.io/en/latest/getting_started.html
    #     'rest_framework_simplejwt.authentication.JWTAuthentication',

            # OAUTH
    #     # # 'oauth2_provider.ext.rest_framework.OAuth2Authentication',  # django-oauth-toolkit < 1.0.0
    #     # # django-oauth-toolkit >= 1.0.0
    #     'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
    #     'drf_social_oauth2.authentication.SocialAuthentication',
    # ),
}
# Schema Generator
# https://www.django-rest-framework.org/api-guide/schemas/

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    # When someone uses refresh token to renew access token then the 
    # refresh token is reset too, so that it expires in 1 day if set to True
    'ROTATE_REFRESH_TOKENS': False,
    # Blacklist keys after they have been utilized
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': False,

    'ALGORITHM': 'HS256',
    # SECRET KEY is declared up above
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,

    # FOR JWT
    'AUTH_HEADER_TYPES': ('JWT'), # JWT, 'Bearer', 
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    # Go to Jwt.io with the token you recieve on signing in
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}

# Custom user model
# Defining to Django this is our new user model which we made when we built the new users app
AUTH_USER_MODEL = "users.NewUser"

AUTHENTICATION_BACKENDS = (
    'drf_social_oauth2.backends.DjangoOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

AUTHENTICATION_BACKENDS = (
    # Others auth providers (e.g. Google, OpenId, etc)

    # Facebook OAuth2
    'social_core.backends.facebook.FacebookAppOAuth2',
    'social_core.backends.facebook.FacebookOAuth2',

    # drf_social_oauth2
    'drf_social_oauth2.backends.DjangoOAuth2',

    # Django
    'django.contrib.auth.backends.ModelBackend',
)

# Facebook configuration
SOCIAL_AUTH_FACEBOOK_KEY = ('424762231818988')
SOCIAL_AUTH_FACEBOOK_SECRET = ('7ea506193526e3f8ecc7743579545e15')
SOCIAL_AUTH_LOGIN_REDIRECT_URL = 'http://localhost:3000/'

# Define SOCIAL_AUTH_FACEBOOK_SCOPE to get extra permissions from Facebook.
# Email is not sent by default, to get it, you must request the email permission.
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
    'fields': 'id, name, email'
}
SOCIAL_AUTH_USER_FIELDS = ['email', 'username', 'first_name', 'password']
