from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [
        migrations.CreateModel(name='Category', fields=[
            ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ('name', models.CharField(max_length=100)),
            ('slug', models.SlugField(unique=True)),
        ]),
        migrations.CreateModel(name='Product', fields=[
            ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ('name', models.CharField(max_length=180)),
            ('slug', models.SlugField(unique=True)),
            ('description', models.TextField(blank=True)),
            ('price', models.DecimalField(decimal_places=2, max_digits=12)),
            ('stock', models.PositiveIntegerField(default=1)),
            ('image', models.ImageField(blank=True, upload_to='products/')),
            ('is_active', models.BooleanField(default=True)),
            ('created_at', models.DateTimeField(auto_now_add=True)),
            ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='products', to='marketplace.category')),
            ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to=settings.AUTH_USER_MODEL)),
        ]),
    ]
