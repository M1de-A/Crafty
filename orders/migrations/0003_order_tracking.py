from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies=[('orders','0002_orderitem')]
    operations=[
        migrations.AddField(model_name='order',name='updated_at',field=models.DateTimeField(auto_now=True)),
        migrations.AddField(model_name='order',name='tracking_number',field=models.CharField(blank=True,max_length=120,verbose_name='Трек-номер')),
        migrations.AddField(model_name='order',name='shipped_at',field=models.DateTimeField(blank=True,null=True)),
        migrations.AddField(model_name='order',name='delivered_at',field=models.DateTimeField(blank=True,null=True)),
    ]
