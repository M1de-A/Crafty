from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.http import url_has_allowed_host_and_scheme
from marketplace.models import Product
from shops.models import Shop
from .forms import ReviewForm
from .models import Favorite, Review, ShopFollow

@login_required
def toggle_favorite(request, slug):
    product=get_object_or_404(Product,slug=slug,is_active=True); favorite,created=Favorite.objects.get_or_create(user=request.user,product=product)
    if not created: favorite.delete()
    next_url=request.POST.get('next','')
    if next_url and url_has_allowed_host_and_scheme(next_url,allowed_hosts={request.get_host()}): return redirect(next_url)
    return redirect('product',slug=slug)

@login_required
def favorites(request):
    products=Product.objects.filter(favorites__user=request.user,is_active=True).select_related('seller','category').annotate(avg_rating=Avg('reviews__rating'),review_count=Count('reviews',distinct=True)).distinct()
    return render(request,'social/favorites.html',{'products':products})

@login_required
def toggle_follow(request, slug):
    shop=get_object_or_404(Shop,slug=slug); follow,created=ShopFollow.objects.get_or_create(user=request.user,shop=shop)
    if not created: follow.delete()
    return redirect(request.POST.get('next') or 'shop',slug=shop.slug)

@login_required
def followed_shops(request):
    shops=Shop.objects.filter(followers__user=request.user).select_related('seller').annotate(follower_count=Count('followers',distinct=True),product_count=Count('seller__products',distinct=True))
    return render(request,'social/followed_shops.html',{'shops':shops})

@login_required
def add_review(request, slug):
    product=get_object_or_404(Product,slug=slug,is_active=True)
    purchased=product.order_items.filter(order__buyer=request.user,order__status__in=['delivered','completed','return']).exists()
    if not purchased:
        messages.error(request,'Оставить отзыв можно после покупки этого товара.'); return redirect('product',slug=slug)
    review=Review.objects.filter(user=request.user,product=product).first()
    if request.method=='POST':
        if review:
            form=ReviewForm(request.POST,instance=review,editing=True)
            if form.is_valid():
                obj=form.save(commit=False); obj.rating=review.rating; obj.save(update_fields=['text','updated_at'])
                messages.success(request,'Текст отзыва дополнен. Оценка уже опубликованного отзыва не изменяется.')
                return redirect('product',slug=slug)
        else:
            form=ReviewForm(request.POST)
            if form.is_valid():
                obj=form.save(commit=False); obj.user=request.user; obj.product=product; obj.save()
                messages.success(request,'Спасибо! Ваш отзыв опубликован.')
                return redirect('product',slug=slug)
    else: form=ReviewForm(instance=review,editing=bool(review))
    return render(request,'social/review_form.html',{'form':form,'product':product,'editing':bool(review),'review':review})
