from django.contrib import admin
from .models import Favorite,Review,ShopFollow
admin.site.register(Favorite)
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display=('product','user','rating','created_at')
    list_filter=('rating','created_at')
@admin.register(ShopFollow)
class ShopFollowAdmin(admin.ModelAdmin):
    list_display=('shop','user','created_at')
