from decimal import Decimal
import uuid
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from marketplace.models import Product
from .models import Order, OrderItem

def _cart(request): return request.session.get('crafty_cart', {})

def cart(request):
    raw=_cart(request); items=[]; total=Decimal('0')
    for key, qty in raw.items():
        product=Product.objects.filter(pk=key,is_active=True).select_related('category').first()
        if not product: continue
        quantity=min(int(qty), product.stock)
        if quantity <= 0: continue
        subtotal=product.price*quantity; total += subtotal
        items.append({'product':product,'quantity':quantity,'subtotal':subtotal})
    return render(request,'orders/cart.html',{'items':items,'total':total})

def add_to_cart(request, pk):
    product=get_object_or_404(Product,pk=pk,is_active=True)
    if request.method != 'POST': return redirect('product', product.slug)
    cart_data=_cart(request).copy(); current=int(cart_data.get(str(pk),0)); requested=max(1,int(request.POST.get('quantity','1')))
    cart_data[str(pk)]=min(current+requested, product.stock); request.session['crafty_cart']=cart_data; request.session.modified=True
    messages.success(request,'Товар добавлен в корзину.')
    return redirect(request.POST.get('next') or 'cart')

def remove_from_cart(request, pk):
    if request.method=='POST':
        cart_data=_cart(request).copy(); cart_data.pop(str(pk),None); request.session['crafty_cart']=cart_data; request.session.modified=True
    return redirect('cart')

@login_required
def checkout(request):
    if request.method!='POST': return redirect('cart')
    raw=_cart(request)
    if not raw: return redirect('cart')
    with transaction.atomic():
        order=Order.objects.create(buyer=request.user,total=Decimal('0'),status='new',payment_status='pending')
        total=Decimal('0')
        for key, qty in raw.items():
            product=Product.objects.select_for_update().filter(pk=key,is_active=True).first()
            if not product: continue
            quantity=min(int(qty),product.stock)
            if quantity<=0: continue
            subtotal=product.price*quantity
            OrderItem.objects.create(order=order,product=product,seller=product.seller,product_name=product.name,unit_price=product.price,quantity=quantity,subtotal=subtotal)
            product.stock-=quantity; product.save(update_fields=['stock']); total+=subtotal
        if total==0:
            order.delete(); messages.error(request,'Не удалось оформить заказ: товары закончились.'); return redirect('cart')
        order.total=total; order.save(update_fields=['total','updated_at'])
    request.session['crafty_cart']={}; request.session.modified=True
    messages.success(request,f'Заказ #{order.id} создан. Теперь его можно оплатить.')
    return redirect('order_detail', order_id=order.id)

@login_required
def orders(request):
    qs=Order.objects.filter(buyer=request.user).prefetch_related('items').order_by('-created_at')
    return render(request,'orders/orders.html',{'orders':qs})

@login_required
def order_detail(request, order_id):
    order=get_object_or_404(Order.objects.prefetch_related('items__product','items__seller'),pk=order_id,buyer=request.user)
    return render(request,'orders/detail.html',{'order':order})

def _payment_client():
    from yookassa import Configuration
    shop_id=getattr(settings,'YOOKASSA_SHOP_ID','')
    secret=getattr(settings,'YOOKASSA_SECRET_KEY','')
    if not shop_id or not secret: raise RuntimeError('ЮKassa не настроена: укажите YOOKASSA_SHOP_ID и YOOKASSA_SECRET_KEY.')
    Configuration.account_id=shop_id; Configuration.secret_key=secret
    from yookassa import Payment
    return Payment

@login_required
def pay_order(request, order_id):
    order=get_object_or_404(Order,pk=order_id,buyer=request.user)
    if order.status!='new':
        messages.info(request,'Этот заказ уже нельзя оплатить повторно.')
        return redirect('order_detail',order_id=order.id)
    try:
        Payment=_payment_client()
        from yookassa import Payment as YooPayment
        payment=YooPayment.create({
            'amount':{'value':f'{order.total:.2f}','currency':'RUB'},
            'capture':True,
            'confirmation':{'type':'redirect','return_url':request.build_absolute_uri(f'/orders/payment/return/{order.id}/')},
            'description':f'Оплата заказа №{order.id}',
            'metadata':{'order_id':str(order.id)},
        }, str(uuid.uuid4()))
        order.payment_id=payment.id; order.payment_status=payment.status; order.save(update_fields=['payment_id','payment_status','updated_at'])
        return redirect(payment.confirmation.confirmation_url)
    except Exception as exc:
        messages.error(request,f'Не удалось создать платёж. Проверьте настройки ЮKassa. ({exc})')
        return redirect('order_detail',order_id=order.id)

@login_required
def payment_return(request, order_id):
    order=get_object_or_404(Order,pk=order_id,buyer=request.user)
    if order.payment_id:
        try:
            Payment=_payment_client(); payment=Payment.find_one(order.payment_id)
            order.payment_status=payment.status
            if payment.status=='succeeded': order.status='paid'
            elif payment.status in {'canceled','cancelled'}: order.payment_status='canceled'
            order.save(update_fields=['status','payment_status','updated_at'])
        except Exception: pass
    return redirect('order_detail',order_id=order.id)

@csrf_exempt
def payment_webhook(request):
    if request.method!='POST': return HttpResponse(status=405)
    try:
        import json
        payload=json.loads(request.body.decode('utf-8'))
        obj=payload.get('object',{})
        payment_id=obj.get('id')
        status=obj.get('status')
        if payment_id:
            order=Order.objects.filter(payment_id=payment_id).first()
            if order:
                order.payment_status=status or order.payment_status
                if status=='succeeded' and order.status=='new': order.status='paid'
                order.save(update_fields=['status','payment_status','updated_at'])
        return HttpResponse(status=200)
    except Exception: return HttpResponse(status=400)

def _restore_stock(order):
    for item in order.items.select_related('product'):
        item.product.stock += item.quantity; item.product.save(update_fields=['stock'])

@login_required
def cancel_order(request, order_id):
    if request.method!='POST': return redirect('order_detail',order_id=order_id)
    order=get_object_or_404(Order,pk=order_id,buyer=request.user)
    if order.status!='processing':
        messages.error(request,'Отменить заказ можно только на этапе сборки.')
        return redirect('order_detail',order_id=order.id)
    reason=request.POST.get('reason','').strip()
    if not reason: messages.error(request,'Укажите причину отмены.'); return redirect('order_detail',order_id=order.id)
    with transaction.atomic():
        _restore_stock(order); order.status='cancelled'; order.cancelled_by='buyer'; order.cancel_reason=reason; order.cancelled_at=timezone.now(); order.save(update_fields=['status','cancelled_by','cancel_reason','cancelled_at','updated_at'])
    messages.success(request,'Заказ отменён.')
    return redirect('order_detail',order_id=order.id)

@login_required
def request_return(request, order_id):
    if request.method!='POST': return redirect('order_detail',order_id=order_id)
    order=get_object_or_404(Order,pk=order_id,buyer=request.user)
    if order.status not in {'delivered','completed'}:
        messages.error(request,'Запрос на возврат доступен после получения заказа.')
        return redirect('order_detail',order_id=order.id)
    reason=request.POST.get('reason','').strip()
    if not reason: messages.error(request,'Укажите причину возврата.'); return redirect('order_detail',order_id=order.id)
    order.status='return'; order.return_reason=reason; order.return_at=timezone.now(); order.save(update_fields=['status','return_reason','return_at','updated_at'])
    messages.success(request,'Запрос на возврат отправлен.')
    return redirect('order_detail',order_id=order.id)

@login_required
def seller_order_update(request, order_id):
    if request.method != 'POST': return redirect('seller_dashboard')
    order=get_object_or_404(Order,pk=order_id)
    if getattr(getattr(request.user,'profile',None),'role',None) != 'seller': return redirect('orders')
    if not OrderItem.objects.filter(order=order,seller=request.user).exists(): return redirect('seller_dashboard')
    status=request.POST.get('status') or order.status; tracking=request.POST.get('tracking_number','').strip()
    allowed={'processing','shipped','delivered','completed','cancelled'}
    if status not in allowed: messages.error(request,'Недопустимый статус заказа.'); return redirect('seller_dashboard')
    if order.status=='new' and status=='processing':
        messages.error(request,'Сначала покупатель должен оплатить заказ.')
        return redirect('seller_dashboard')
    if status=='cancelled' and order.status!='processing':
        messages.error(request,'Продавец может отменить заказ только на этапе сборки.'); return redirect('seller_dashboard')
    if order.status in {'cancelled','return','completed'} and status != order.status:
        messages.error(request,'Этот заказ больше нельзя изменить на данный статус.'); return redirect('seller_dashboard')
    if status=='cancelled':
        reason=request.POST.get('reason','').strip()
        if not reason: messages.error(request,'Укажите причину отмены.'); return redirect('seller_dashboard')
        _restore_stock(order); order.cancelled_by='seller'; order.cancel_reason=reason; order.cancelled_at=timezone.now()
    order.status=status
    if tracking: order.tracking_number=tracking
    if status=='shipped' and not order.shipped_at: order.shipped_at=timezone.now()
    if status in {'delivered','completed'} and not order.delivered_at: order.delivered_at=timezone.now()
    order.save(update_fields=['status','tracking_number','shipped_at','delivered_at','cancelled_by','cancel_reason','cancelled_at','updated_at'])
    messages.success(request,f'Заказ #{order.id} обновлён.')
    return redirect('seller_dashboard')
