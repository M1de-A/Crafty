from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import register,account,site_login
urlpatterns=[path('',account,name='account'),path('login/',site_login,name='login'),path('logout/',LogoutView.as_view(),name='logout'),path('register/',register,name='register')]
