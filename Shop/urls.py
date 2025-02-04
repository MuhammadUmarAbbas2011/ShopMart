from django.urls import path
from .views import *

urlpatterns = [
    path('', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('products/', product_list, name='products'),
    path('add_to_cart/<int:id>/', add_to_cart, name='add_to_cart'),
    path('cart/', view_cart, name='view_cart'),
    path('delete_from_cart/<int:id>/',delete_items_from_cart,name="delete_from_cart")
]
