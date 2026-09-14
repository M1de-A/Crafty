from django.contrib.auth.models import User
from django.db import models
from marketplace.models import Product
from shops.models import Shop

class Favorite(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='favorites')
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name='favorites')
    created_at=models.DateTimeField(auto_now_add=True)
    class Meta:
        constraints=[models.UniqueConstraint(fields=['user','product'],name='unique_favorite_user_product')]
        ordering=['-created_at']
    def __str__(self): return f'{self.user} → {self.product}'

class Review(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='product_reviews')
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name='reviews')
    rating=models.DecimalField(max_digits=2,decimal_places=1,choices=[(i/2,f'{i/2:g}') for i in range(1,11)])
    text=models.TextField(blank=True,max_length=1500)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    class Meta:
        constraints=[models.UniqueConstraint(fields=['user','product'],name='unique_review_user_product')]
        ordering=['-created_at']
    def __str__(self): return f'{self.product}: {self.rating}/5'

class ShopFollow(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='followed_shops')
    shop=models.ForeignKey(Shop,on_delete=models.CASCADE,related_name='followers')
    created_at=models.DateTimeField(auto_now_add=True)
    class Meta:
        constraints=[models.UniqueConstraint(fields=['user','shop'],name='unique_shop_follow_user_shop')]
        ordering=['-created_at']
    def __str__(self): return f'{self.user} → {self.shop}'
