from django.urls import path
from .views import create_product, get_my_products, get_all_products, vendor_add_products, edit_product, delete_product, product_details, landing_page
urlpatterns = [
    path('create/', create_product, name = 'add_product'),
    path('my_products/', get_my_products, name = 'vendor_products'),
    path('add_products/', vendor_add_products, name = 'vendor_add_products'),
    path('edit_product/', edit_product, name="edit_product"),
    path('delete_product/', delete_product, name='delete_product'),
    path('product_details/', product_details, name='product_details'),
    path('products/', get_all_products, name='all_products'),
    # path('', landing_page, name='landing_page'),

]