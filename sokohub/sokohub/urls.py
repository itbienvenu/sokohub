from django.contrib import admin
from django.urls import path, include
from Product.views import get_all_products, landing_page

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('Account.urls')),
    path('products/', include('Product.urls')),
    path('', landing_page, name="landing_page"),
    path("orders/", include('Orders.urls'))
]

