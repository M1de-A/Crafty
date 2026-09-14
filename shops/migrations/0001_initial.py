from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [migrations.CreateModel(
        name='Shop',
        fields=[
            ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ('name', models.CharField(max_length=120)),
            ('slug', models.SlugField(unique=True)),
            ('description', models.TextField(blank=True)),
            ('seller', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='shop', to=settings.AUTH_USER_MODEL)),
        ],
    )]
