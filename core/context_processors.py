def site_preferences(request):
    lang=request.session.get('crafty_language','ru')
    currency=request.session.get('crafty_currency','RUB')
    cart=request.session.get('crafty_cart',{})
    cart_count=sum(int(v) for v in cart.values()) if cart else 0
    favorite_count=followed_count=0
    if request.user.is_authenticated:
        try:
            from social.models import Favorite, ShopFollow
            favorite_count=Favorite.objects.filter(user=request.user).count()
            followed_count=ShopFollow.objects.filter(user=request.user).count()
        except Exception:
            pass
    return {'CRAFTY_LANGUAGE':lang,'CRAFTY_CURRENCY':currency,'LANGUAGES_AVAILABLE':[('ru','Русский'),('en','English')],'CURRENCIES_AVAILABLE':[('RUB','₽ RUB')],'CART_COUNT':cart_count,'FAVORITE_COUNT':favorite_count,'FOLLOWED_SHOP_COUNT':followed_count}
