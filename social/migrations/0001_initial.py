from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial=True
    dependencies=[
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('marketplace','0001_initial'),
        ('shops','0001_initial'),
        ('orders','0002_orderitem'),
    ]
    operations=[
        migrations.CreateModel(name='Favorite',fields=[('id',models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name='ID')),('created_at',models.DateTimeField(auto_now_add=True)),('product',models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,related_name='favorites',to='marketplace.product')),('user',models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,related_name='favorites',to=settings.AUTH_USER_MODEL))],options={'ordering':['-created_at']}),
        migrations.CreateModel(name='Review',fields=[('id',models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name='ID')),('rating',models.PositiveSmallIntegerField(choices=[(1,'1'),(2,'2'),(3,'3'),(4,'4'),(5,'5')])),('text',models.TextField(blank=True,max_length=1500)),('created_at',models.DateTimeField(auto_now_add=True)),('updated_at',models.DateTimeField(auto_now=True)),('product',models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,related_name='reviews',to='marketplace.product')),('user',models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,related_name='product_reviews',to=settings.AUTH_USER_MODEL))],options={'ordering':['-created_at']}),
        migrations.CreateModel(name='ShopFollow',fields=[('id',models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name='ID')),('created_at',models.DateTimeField(auto_now_add=True)),('shop',models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,related_name='followers',to='shops.shop')),('user',models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,related_name='followed_shops',to=settings.AUTH_USER_MODEL))],options={'ordering':['-created_at']}),
        migrations.AddConstraint(model_name='favorite',constraint=models.UniqueConstraint(fields=('user','product'),name='unique_favorite_user_product')),
        migrations.AddConstraint(model_name='review',constraint=models.UniqueConstraint(fields=('user','product'),name='unique_review_user_product')),
        migrations.AddConstraint(model_name='shopfollow',constraint=models.UniqueConstraint(fields=('user','shop'),name='unique_shop_follow_user_shop')),
    ]
