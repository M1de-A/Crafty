from django.contrib import admin
from django.utils import timezone
from .models import Order,OrderItem

@admin.action(description='✓ Заказ получен: отметить как доставленный')
def mark_received(modeladmin,request,queryset):
    now=timezone.now()
    updated=queryset.exclude(status__in=['cancelled','dispute','completed']).update(status='delivered',delivered_at=now)
    modeladmin.message_user(request,f'Заказов отмечено полученными: {updated}.')

@admin.action(description='📦 Перевести выбранные заказы в «Отправлен»')
def mark_shipped(modeladmin,request,queryset):
    now=timezone.now()
    updated=queryset.exclude(status__in=['cancelled','dispute','completed','delivered']).update(status='shipped',shipped_at=now)
    modeladmin.message_user(request,f'Заказов отмечено отправленными: {updated}.')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display=('id','buyer','status','total','tracking_number','created_at','delivered_at')
    list_filter=('status','created_at')
    search_fields=('=id','buyer__username','buyer__email','tracking_number')
    readonly_fields=('created_at','updated_at','shipped_at','delivered_at')
    actions=[mark_received,mark_shipped]

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display=('order','product_name','seller','quantity','unit_price','subtotal')
    list_filter=('seller',)
    search_fields=('product_name','seller__username')
