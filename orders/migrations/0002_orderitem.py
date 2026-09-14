from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies=[('orders','0001_initial'),('marketplace','0001_initial'),]
    operations=[migrations.CreateModel(name='OrderItem',fields=[
        ('id',models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name='ID')),
        ('product_name',models.CharField(max_length=180)),
        ('unit_price',models.DecimalField(decimal_places=2,max_digits=12)),
        ('quantity',models.PositiveIntegerField(default=1)),
        ('subtotal',models.DecimalField(decimal_places=2,max_digits=12)),
        ('order',models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,related_name='items',to='orders.order')),
        ('product',models.ForeignKey(on_delete=django.db.models.deletion.PROTECT,related_name='order_items',to='marketplace.product')),
        ('seller',models.ForeignKey(on_delete=django.db.models.deletion.PROTECT,related_name='seller_order_items',to='auth.user')),
    ])]
