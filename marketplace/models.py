from django.db import models
from django.contrib.auth.models import User
class Category(models.Model):
    name=models.CharField(max_length=100); slug=models.SlugField(unique=True)
    def __str__(self):return self.name
class Product(models.Model):
    seller=models.ForeignKey(User,on_delete=models.CASCADE,related_name='products')
    category=models.ForeignKey(Category,on_delete=models.SET_NULL,null=True,blank=True,related_name='products')
    name=models.CharField(max_length=180); slug=models.SlugField(unique=True); description=models.TextField(blank=True)
    price=models.DecimalField(max_digits=12,decimal_places=2); stock=models.PositiveIntegerField(default=1); image=models.ImageField(upload_to='products/',blank=True)
    is_active=models.BooleanField(default=True); created_at=models.DateTimeField(auto_now_add=True)
    def __str__(self):return self.name
