from django.db import models
from django.contrib.auth.models import User
from django.db.models.functions import Lower

class Shop(models.Model):
    seller=models.OneToOneField(User,on_delete=models.CASCADE,related_name='shop')
    name=models.CharField(max_length=120)
    slug=models.SlugField(unique=True)
    description=models.TextField(blank=True)
    avatar=models.ImageField(upload_to='shops/avatars/',blank=True)
    banner=models.ImageField(upload_to='shops/banners/',blank=True)
    class Meta:
        constraints=[models.UniqueConstraint(Lower('name'),name='unique_shop_name_ci')]
    def __str__(self):return self.name
