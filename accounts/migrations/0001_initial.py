from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [migrations.CreateModel(
        name='Profile',
        fields=[
            ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ('role', models.CharField(choices=[('buyer','Покупатель'),('seller','Продавец')], default='buyer', max_length=20)),
            ('verification_status', models.CharField(default='not_started', max_length=20)),
            ('verification_level', models.CharField(default='new', max_length=30)),
            ('trust_score', models.PositiveSmallIntegerField(default=0)),
            ('free_showcases', models.PositiveIntegerField(default=5)),
            ('promotion_priority', models.PositiveSmallIntegerField(default=0)),
            ('payout_priority', models.BooleanField(default=False)),
            ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
        ],
    )]
