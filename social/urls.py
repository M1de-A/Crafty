from django.urls import path
from .views import toggle_favorite,favorites,toggle_follow,followed_shops,add_review
urlpatterns=[
 path('favorites/',favorites,name='favorites'),
 path('favorites/<slug:slug>/toggle/',toggle_favorite,name='toggle_favorite'),
 path('shops/followed/',followed_shops,name='followed_shops'),
 path('shops/<slug:slug>/follow/',toggle_follow,name='toggle_follow'),
 path('reviews/<slug:slug>/add/',add_review,name='add_review'),
]
