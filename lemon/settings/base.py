"""
Django settings for lemon project.
Generated by 'django-admin startproject' using Django 3.2.9.
For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/
For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
import os, json
from mysettings import SECRET_KEY, MY_DATABASES

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = SECRET_KEY

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['52.78.138.222']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sites',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'accounts',
    'calendars',
    'admins',
    'rest_framework',
    'corsheaders',
    'ckeditor',
    'ckeditor_uploader',
    'stocks',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.auth0',
    'allauth.socialaccount.providers.kakao',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.naver',
]

LOGIN_REDIRECT_URL = '/' # 로그인 후 리디렉션할 페이지
ACCOUNT_LOGOUT_REDIRECT_URL = "/"  # 로그아웃 후 리디렉션 할 페이지
ACCOUNT_LOGOUT_ON_GET = True # 로그아웃 버튼 클릭 시 자동 로그아웃
ACCOUNT_AUTHENTICATED_LOGIN_REDIRECTS = True
ACCOUNT_USER_MODEL_EMAIL_FIELD: None
ACCOUNT_EMAIL_REQUIRED: False 
SOCIALACCOUNT_AUTO_SIGNUP = True # 디폴트 값은 True이며 SNS 공급자에서 넘겨받은 정보를 가지고 바로 회원가입시킨다. 부가정보를 입력 받기 위해 False로 설정할 수 있다.
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',  # <- 디폴트 모델 백엔드
    'allauth.account.auth_backends.AuthenticationBackend', # <- 추가
)


SITE_ID = 1

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'lemon.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
            #os.path.join(BASE_DIR, 'templates', 'allauth'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.media',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

SESSION_COOKIE_SECURE = False

WSGI_APPLICATION = 'lemon.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases
DATABASES = MY_DATABASES

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators
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
# https://docs.djangoproject.com/en/3.2/topics/i18n/
LANGUAGE_CODE = 'ko-kr'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_L10N = True

USE_TZ = False

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/login'
SIGNUP_REDIRECT_URL = '/signup'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'accounts', 'static'),
)
'''
STATIC_DIR = [
    os.path.join(BASE_DIR, '' 'static')
]
'''
# 배포서버에서 static 파일을 모아서 관리하는 폴더명
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_ROOT = 'media/'
MEDIA_URL = '/media/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'accounts.user'

CORS_ORIGIN_ALLOW_ALL = True
#AUTHENTICATION_BACKENDS = ('accounts.models.LemonUserAuth',)

# CKEDITOR Settings
CKEDITOR_UPLOAD_PATH = 'notices/'
CKEDITOR_RESTRICT_BY_USER = True
CKEDITOR_IMAGE_BACKEND = 'pillow'
CKEDITOR_CONFIGS = {
    'default': {
        'autoParagraph': False,
        'toolbar': 'custom',
        'toolbar_custom': [
            ['Font', 'FontSize', 'Format'],
            ['Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript', '-', 'RemoveFormat'],
            [
                'NumberedList', 'BulletedList', '-',
                'Outdent', 'Indent', '-',
                'Blockquote', '-',
                'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock'
            ],
            ['Link', 'Unlink', 'Anchor'],
            ['Image', 'Flash', 'Table', 'HorizontalRule', 'PageBreak', 'Smiley', 'SpecialChar'],
            ['Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord', '-', 'Undo', 'Redo'],
            ['TextColor', 'BGColor'],
            ['Maximize', 'Source'],
        ],
    },
}