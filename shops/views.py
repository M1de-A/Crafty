from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from .forms import ShopForm, ProductForm
from .models import Shop
from marketplace.models import Product
from django.db.models import Avg, Count
from social.models import ShopFollow
from orders.models import OrderItem

@login_required
def seller_dashboard(request):
    profile=request.user.profile
    if profile.role!='seller': return redirect('become_seller')
    shop=getattr(request.user,'shop',None)
    products=Product.objects.filter(seller=request.user).select_related('category').order_by('-created_at')
    seller_items=OrderItem.objects.filter(seller=request.user).select_related('order','product','order__buyer').order_by('-order__created_at')
    orders={item.order_id:item.order for item in seller_items}
    return render(request,'shops/dashboard.html',{'profile':profile,'shop':shop,'products':products,'seller_items':seller_items,'seller_orders':list(orders.values())})

@login_required
def become_seller(request):
    profile=request.user.profile
    if profile.role=='seller': return redirect('seller_dashboard')
    if request.method=='POST':
        profile.role='seller'; profile.save(update_fields=['role']); messages.success(request,'Теперь вы продавец. Создайте витрину и добавьте первый товар!'); return redirect('shop_create')
    return render(request,'shops/become_seller.html')

@login_required
def shop_create(request):
    if request.user.profile.role!='seller': return redirect('become_seller')
    if hasattr(request.user,'shop'): return redirect('seller_dashboard')
    form=ShopForm(request.POST or None, request.FILES or None)
    if request.method=='POST' and form.is_valid():
        shop=form.save(commit=False); shop.seller=request.user; shop.save(); messages.success(request,'Магазин создан.'); return redirect('seller_dashboard')
    return render(request,'shops/shop_form.html',{'form':form,'title':'Создать магазин'})

@login_required
def product_create(request):
    if request.user.profile.role!='seller': return redirect('become_seller')
    if not hasattr(request.user,'shop'): return redirect('shop_create')
    form=ProductForm(request.POST or None,request.FILES or None)
    if request.method=='POST' and form.is_valid():
        product=form.save(commit=False); product.seller=request.user; product.save(); messages.success(request,'Товар сохранён.'); return redirect('seller_dashboard')
    return render(request,'shops/product_form.html',{'form':form,'title':'Добавить товар'})

@login_required
def product_edit(request,pk):
    product=get_object_or_404(Product,pk=pk,seller=request.user); form=ProductForm(request.POST or None,request.FILES or None,instance=product)
    if request.method=='POST' and form.is_valid(): form.save(); messages.success(request,'Товар обновлён.'); return redirect('seller_dashboard')
    return render(request,'shops/product_form.html',{'form':form,'title':'Редактировать товар','product':product})

@login_required
def product_delete(request,pk):
    product=get_object_or_404(Product,pk=pk,seller=request.user)
    if request.method=='POST': product.delete(); messages.success(request,'Товар удалён.'); return redirect('seller_dashboard')
    return render(request,'shops/product_delete.html',{'product':product})

def shop(request,slug):
    shop=get_object_or_404(Shop,slug=slug); products=Product.objects.filter(seller=shop.seller,is_active=True).select_related('category').annotate(avg_rating=Avg('reviews__rating'),review_count=Count('reviews',distinct=True)).order_by('-created_at')
    is_following=request.user.is_authenticated and ShopFollow.objects.filter(user=request.user,shop=shop).exists()
    return render(request,'shops/shop.html',{'shop':shop,'products':products,'is_following':is_following,'follower_count':shop.followers.count()})
