from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [migrations.CreateModel(
        name='Order',
        fields=[
            ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ('status', models.CharField(choices=[('new','Новый'),('paid','Оплачен'),('processing','В обработке'),('shipped','Отправлен'),('delivered','Доставлен'),('completed','Завершён'),('cancelled','Отменён'),('dispute','Спор')], default='new', max_length=20)),
            ('total', models.DecimalField(decimal_places=2, max_digits=12)),
            ('created_at', models.DateTimeField(auto_now_add=True)),
            ('buyer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='orders', to=settings.AUTH_USER_MODEL)),
        ],
    )]
