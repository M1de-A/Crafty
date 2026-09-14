from django.contrib.auth.models import User
from django.db import models
from marketplace.models import Product

class Order(models.Model):
    STATUS=[
        ('new','Ожидает оплаты'),
        ('paid','Оплачен'),
        ('processing','Сборка'),
        ('shipped','Отправлен'),
        ('delivered','Доставлен'),
        ('completed','Завершён'),
        ('cancelled','Отменён'),
        ('return','Возврат'),
        ('dispute','Спор'),
    ]
    CANCELLED_BY=[('buyer','Покупатель'),('seller','Продавец'),('admin','Администратор'),('system','Система')]
    buyer=models.ForeignKey(User,on_delete=models.PROTECT,related_name='orders')
    status=models.CharField(max_length=20,choices=STATUS,default='new')
    total=models.DecimalField(max_digits=12,decimal_places=2)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    tracking_number=models.CharField('Трек-номер',max_length=120,blank=True)
    shipped_at=models.DateTimeField(null=True,blank=True)
    delivered_at=models.DateTimeField(null=True,blank=True)
    cancelled_at=models.DateTimeField(null=True,blank=True)
    cancelled_by=models.CharField(max_length=20,choices=CANCELLED_BY,blank=True)
    cancel_reason=models.CharField(max_length=500,blank=True)
    return_at=models.DateTimeField(null=True,blank=True)
    return_reason=models.CharField(max_length=500,blank=True)
    payment_id=models.CharField(max_length=120,blank=True,unique=True,null=True)
    payment_status=models.CharField(max_length=30,default='pending')

    def __str__(self): return f'Заказ #{self.id}'

class OrderItem(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE,related_name='items')
    product=models.ForeignKey(Product,on_delete=models.PROTECT,related_name='order_items')
    seller=models.ForeignKey(User,on_delete=models.PROTECT,related_name='seller_order_items')
    product_name=models.CharField(max_length=180)
    unit_price=models.DecimalField(max_digits=12,decimal_places=2)
    quantity=models.PositiveIntegerField(default=1)
    subtotal=models.DecimalField(max_digits=12,decimal_places=2)
    def __str__(self): return f'{self.product_name} × {self.quantity}'
