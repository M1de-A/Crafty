from django.urls import path
from .views import catalog,product
urlpatterns=[path('',catalog,name='catalog'),path('<slug:slug>/',product,name='product')]
