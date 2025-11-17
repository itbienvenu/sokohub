from django.contrib import admin
from django.urls import path, include
from Product.views import get_all_products

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('Account.urls')),
    path('products/', include('Product.urls')),
    path('', get_all_products, name="all_products"),
    path("orders/", include('Orders.urls'))
]

