from django.db import migrations, models
class Migration(migrations.Migration):
    dependencies=[('shops','0001_initial')]
    operations=[
        migrations.AddField(model_name='shop',name='avatar',field=models.ImageField(blank=True,upload_to='shops/avatars/')),
        migrations.AddField(model_name='shop',name='banner',field=models.ImageField(blank=True,upload_to='shops/banners/')),
    ]
