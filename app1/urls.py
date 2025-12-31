from django.urls import path
from .views import *

urlpatterns = [
    path('', product_list, name='product_list'),
    path('add-product/', add_product, name='add_product'),
    path('products/', read_products, name='read_products'),
    path('delete_product/<int:pid>/',delete_product,name='delete_product'),

    path('cart/', read_cart, name='read_cart'),
    path('add-cart/<int:pid>/', add_cart, name='add_cart'),
    path('inc-cart/<int:pid>/', increase_cart, name='inc_cart'),
    path('dec-cart/<int:pid>/', decrease_cart, name='dec_cart'),
    path('remove-cart/<int:pid>/', remove_cart, name='remove_cart'),
    path('clear-cart/', clear_cart, name='clear_cart'),


    
    path('login/', login_user, name='login_user'),
    path('logout/', logout_user, name='logout_user'),
    path('register/', register, name='register'),
    

    path('user-cart/', read_cart_user, name='read_cart_user'),
    path('user-add-cart/<int:pid>/', add_cart_user, name='add_cart_user'),
    path('user-inc-cart/<int:pid>/', increase_cart_user, name='inc_cart_user'),
    path('user-dec-cart/<int:pid>/', decrease_cart_user, name='dec_cart_user'),
    path('user-remove-cart/<int:pid>/', remove_cart_user, name='remove_cart_user'),
    path('user-clear-cart/', clear_cart_user, name='clear_cart_user'),
]