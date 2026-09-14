from django.urls import path
from .views import set_language, set_currency
urlpatterns = [path('language/', set_language, name='set_language'), path('currency/', set_currency, name='set_currency')]
