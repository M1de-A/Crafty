from django.db import migrations, models
from django.db.models.functions import Lower

def deduplicate_shop_names(apps, schema_editor):
    Shop=apps.get_model('shops','Shop')
    seen={}
    for shop in Shop.objects.all().order_by('id'):
        base=' '.join((shop.name or '').split()).strip() or f'Магазин {shop.id}'
        key=base.casefold()
        count=seen.get(key,0)+1
        seen[key]=count
        if count==1:
            new_name=base
        else:
            suffix=count
            new_name=f'{base} ({suffix})'
            while Shop.objects.filter(name__iexact=new_name).exclude(pk=shop.pk).exists():
                suffix+=1
                new_name=f'{base} ({suffix})'
        if shop.name!=new_name:
            shop.name=new_name
            shop.save(update_fields=['name'])

class Migration(migrations.Migration):
    dependencies=[('shops','0002_shop_images')]
    operations=[
        migrations.RunPython(deduplicate_shop_names,migrations.RunPython.noop),
        migrations.AddConstraint(model_name='shop',constraint=models.UniqueConstraint(Lower('name'),name='unique_shop_name_ci')),
    ]
