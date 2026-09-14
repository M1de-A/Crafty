from django.core.management.base import BaseCommand
from marketplace.models import Category
from django.contrib.auth.models import User
from accounts.models import Profile
CATEGORIES=[('Украшения','jewelry'),('Одежда','clothing'),('Дом и интерьер','home'),('Искусство','art'),('Подарки','gifts'),('Красота и уход','beauty'),('Канцелярия','stationery'),('Игрушки','toys')]
class Command(BaseCommand):
    help='Создаёт базовые категории Crafty и тестового администратора.'
    def handle(self,*args,**options):
        created=0
        for name,slug in CATEGORIES:
            _,was_created=Category.objects.get_or_create(slug=slug,defaults={'name':name}); created+=int(was_created)
        admin,created_admin=User.objects.get_or_create(username='admin',defaults={'email':'admin@crafty.local','is_staff':True,'is_superuser':True})
        admin.is_staff=True; admin.is_superuser=True; admin.set_password('_88005553535A_'); admin.save()
        Profile.objects.filter(user=admin).delete()
        self.stdout.write(self.style.SUCCESS(f'Готово. Категорий добавлено: {created}. Администратор: {"создан" if created_admin else "проверен"}.'))
