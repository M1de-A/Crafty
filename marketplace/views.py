from decimal import Decimal
from django.core.paginator import Paginator
from django.db.models import Q, Avg, Count
from django.shortcuts import render,get_object_or_404
from .models import Product,Category

def product_stats(qs):
    return qs.annotate(avg_rating=Avg("reviews__rating"),review_count=Count("reviews",distinct=True))

def home(request):
    products=product_stats(Product.objects.filter(is_active=True).select_related("category","seller").order_by("-created_at")[:8])
    categories=Category.objects.all()[:8]
    return render(request,"marketplace/home.html",{"products":products,"categories":categories})

def catalog(request):
    qs=product_stats(Product.objects.filter(is_active=True).select_related("category","seller"))
    q=request.GET.get("q","").strip(); cat=request.GET.get("category","").strip(); sort=request.GET.get("sort","new")
    min_price=request.GET.get("min_price","").strip(); max_price=request.GET.get("max_price","").strip(); min_rating=request.GET.get("min_rating","").strip(); availability=request.GET.get("availability","").strip()
    if q: qs=qs.filter(Q(name__icontains=q)|Q(description__icontains=q)|Q(seller__username__icontains=q)|Q(seller__shop__name__icontains=q))
    if cat: qs=qs.filter(category__slug=cat)
    if min_price:
        try: qs=qs.filter(price__gte=Decimal(min_price))
        except: pass
    if max_price:
        try: qs=qs.filter(price__lte=Decimal(max_price))
        except: pass
    if min_rating:
        try: qs=qs.filter(avg_rating__gte=Decimal(min_rating))
        except: pass
    if availability=='in': qs=qs.filter(stock__gt=0)
    if sort=='price_asc': ordering='price'
    elif sort=='price_desc': ordering='-price'
    elif sort=='rating': ordering='-avg_rating'
    elif sort=='reviews': ordering='-review_count'
    else: ordering='-created_at'
    paginator=Paginator(qs.order_by(ordering),12); page_obj=paginator.get_page(request.GET.get('page'))
    return render(request,"marketplace/catalog.html",{"products":page_obj.object_list,"page_obj":page_obj,"categories":Category.objects.all(),"q":q,"selected_category":cat,"sort":sort,"min_price":min_price,"max_price":max_price,"min_rating":min_rating,"availability":availability})

def product(request,slug):
    product=get_object_or_404(product_stats(Product.objects.filter(is_active=True).select_related("category","seller")),slug=slug)
    from social.models import Favorite, Review
    is_favorite=request.user.is_authenticated and Favorite.objects.filter(user=request.user,product=product).exists()
    reviews=product.reviews.select_related("user").all()
    purchased=request.user.is_authenticated and product.order_items.filter(order__buyer=request.user,order__status__in=["delivered","completed"]).exists()
    similar=product_stats(Product.objects.filter(is_active=True,category=product.category).exclude(pk=product.pk).select_related("category","seller").order_by("-created_at")[:4]) if product.category else product_stats(Product.objects.filter(is_active=True).exclude(pk=product.pk).select_related("category","seller").order_by("-created_at")[:4])
    return render(request,"marketplace/product.html",{"product":product,"is_favorite":is_favorite,"reviews":reviews,"purchased":purchased,"similar_products":similar})
