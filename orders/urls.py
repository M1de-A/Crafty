from django.urls import path
from .views import cart,add_to_cart,remove_from_cart,checkout,orders,order_detail,seller_order_update,pay_order,payment_return,payment_webhook,cancel_order,request_return
urlpatterns=[
 path('',orders,name='orders'),path('cart/',cart,name='cart'),path('cart/add/<int:pk>/',add_to_cart,name='add_to_cart'),path('cart/remove/<int:pk>/',remove_from_cart,name='remove_from_cart'),path('checkout/',checkout,name='checkout'),
 path('payment/<int:order_id>/',pay_order,name='pay_order'),path('payment/return/<int:order_id>/',payment_return,name='payment_return'),path('payment/webhook/',payment_webhook,name='payment_webhook'),
 path('<int:order_id>/cancel/',cancel_order,name='cancel_order'),path('<int:order_id>/return/',request_return,name='request_return'),path('<int:order_id>/',order_detail,name='order_detail'),path('seller/<int:order_id>/update/',seller_order_update,name='seller_order_update'),
]
