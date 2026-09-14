from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies=[('orders','0003_order_tracking')]
    operations=[
        migrations.AddField(model_name='order',name='cancelled_at',field=models.DateTimeField(blank=True,null=True)),
        migrations.AddField(model_name='order',name='cancelled_by',field=models.CharField(blank=True,choices=[('buyer','Покупатель'),('seller','Продавец'),('admin','Администратор'),('system','Система')],max_length=20)),
        migrations.AddField(model_name='order',name='cancel_reason',field=models.CharField(blank=True,max_length=500)),
        migrations.AddField(model_name='order',name='return_at',field=models.DateTimeField(blank=True,null=True)),
        migrations.AddField(model_name='order',name='return_reason',field=models.CharField(blank=True,max_length=500)),
        migrations.AddField(model_name='order',name='payment_id',field=models.CharField(blank=True,max_length=120,null=True,unique=True)),
        migrations.AddField(model_name='order',name='payment_status',field=models.CharField(default='pending',max_length=30)),
    ]
