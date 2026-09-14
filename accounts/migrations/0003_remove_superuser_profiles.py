from django.db import migrations

def remove_superuser_profiles(apps, schema_editor):
    Profile=apps.get_model('accounts','Profile')
    User=apps.get_model('auth','User')
    Profile.objects.filter(user__is_superuser=True).delete()

class Migration(migrations.Migration):
    dependencies=[('accounts','0002_profile_avatar')]
    operations=[migrations.RunPython(remove_superuser_profiles,migrations.RunPython.noop)]
