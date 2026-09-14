from django.db import migrations, models
class Migration(migrations.Migration):
    dependencies=[('social','0001_initial')]
    operations=[migrations.AlterField(model_name='review',name='rating',field=models.DecimalField(choices=[(i/2,f'{i/2:g}') for i in range(1,11)],decimal_places=1,max_digits=2))]
