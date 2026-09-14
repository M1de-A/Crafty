from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from marketplace.views import home
urlpatterns=[path('preferences/', include('core.urls')), path('admin/',admin.site.urls),path('',home,name='home'),path('account/',include('accounts.urls')),path('catalog/',include('marketplace.urls')),path('shops/',include('shops.urls')),path('orders/',include('orders.urls')),path('social/',include('social.urls'))]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
