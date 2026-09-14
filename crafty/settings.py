from pathlib import Path
import os
from dotenv import load_dotenv
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR/'.env')
SECRET_KEY=os.getenv('SECRET_KEY','dev-secret-key-change-me')
DEBUG=os.getenv('DEBUG','True').lower()=='true'
ALLOWED_HOSTS=['127.0.0.1','localhost']
INSTALLED_APPS=['django.contrib.admin','django.contrib.auth','django.contrib.contenttypes','django.contrib.sessions','django.contrib.messages','django.contrib.staticfiles','accounts.apps.AccountsConfig','marketplace','shops','orders','core','social']
MIDDLEWARE=['django.middleware.security.SecurityMiddleware','django.contrib.sessions.middleware.SessionMiddleware',
'django.middleware.locale.LocaleMiddleware','django.middleware.common.CommonMiddleware','django.middleware.csrf.CsrfViewMiddleware','django.contrib.auth.middleware.AuthenticationMiddleware','django.contrib.messages.middleware.MessageMiddleware','django.middleware.clickjacking.XFrameOptionsMiddleware']
ROOT_URLCONF='crafty.urls'
TEMPLATES=[{'BACKEND':'django.template.backends.django.DjangoTemplates','DIRS':[BASE_DIR/'templates'],'APP_DIRS':True,'OPTIONS':{'context_processors':['django.template.context_processors.request','django.contrib.auth.context_processors.auth','django.contrib.messages.context_processors.messages','core.context_processors.site_preferences']}}]
WSGI_APPLICATION='crafty.wsgi.application'
if os.getenv('DB_ENGINE','sqlite')=='postgres':
    DATABASES={'default':{'ENGINE':'django.db.backends.postgresql','NAME':os.getenv('DB_NAME','crafty'),'USER':os.getenv('DB_USER','postgres'),'PASSWORD':os.getenv('DB_PASSWORD','postgres'),'HOST':os.getenv('DB_HOST','127.0.0.1'),'PORT':os.getenv('DB_PORT','5432')}}
else:
    DATABASES={'default':{'ENGINE':'django.db.backends.sqlite3','NAME':BASE_DIR/'db.sqlite3'}}
AUTH_PASSWORD_VALIDATORS=[]
LANGUAGE_CODE='ru-ru'; TIME_ZONE='Europe/Moscow'; USE_I18N=True; USE_TZ=True
LANGUAGES=[('ru','Русский'),('en','English')]
CURRENCIES={'RUB': {'symbol':'₽','name':'Российский рубль'}}

STATIC_URL='static/'; STATICFILES_DIRS=[BASE_DIR/'static']; STATIC_ROOT=BASE_DIR/'staticfiles'
YOOKASSA_SHOP_ID=os.getenv('YOOKASSA_SHOP_ID','')
YOOKASSA_SECRET_KEY=os.getenv('YOOKASSA_SECRET_KEY','')
MEDIA_URL='/media/'; MEDIA_ROOT=BASE_DIR/'media'
DEFAULT_AUTO_FIELD='django.db.models.BigAutoField'
LOGIN_REDIRECT_URL='/account/'; LOGOUT_REDIRECT_URL='/'
