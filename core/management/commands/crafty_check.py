from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.db import connection
class Command(BaseCommand):
    help='Проверяет состояние Crafty и наличие таблиц приложения.'
    def handle(self,*args,**options):
        call_command('check',verbosity=0)
        tables=set(connection.introspection.table_names())
        required={'accounts_profile','marketplace_category','marketplace_product','shops_shop','orders_order','orders_orderitem','social_favorite','social_review','social_shopfollow'}
        missing=sorted(required-tables)
        if missing:
            self.stdout.write(self.style.ERROR('Не хватает таблиц: '+', '.join(missing))); self.stdout.write('Запустите: python manage.py migrate'); raise SystemExit(1)
        self.stdout.write(self.style.SUCCESS('Crafty check: OK'))
