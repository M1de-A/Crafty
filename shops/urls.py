from django.urls import path
from .views import shop, seller_dashboard, become_seller, shop_create, product_create, product_edit, product_delete

urlpatterns = [
    path('seller/', seller_dashboard, name='seller_dashboard'),
    path('become-seller/', become_seller, name='become_seller'),
    path('create/', shop_create, name='shop_create'),
    path('products/new/', product_create, name='product_create'),
    path('products/<int:pk>/edit/', product_edit, name='product_edit'),
    path('products/<int:pk>/delete/', product_delete, name='product_delete'),
    path('<slug:slug>/', shop, name='shop'),
]
