from django.urls import path
from .views import *

urlpatterns = [
    path('', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('products/', product_list, name='products'),
    path('add_to_cart/<int:id>/', add_to_cart, name='add_to_cart'),
    path('cart/', view_cart, name='view_cart'),
    path('delete_from_cart/<int:id>/',delete_items_from_cart,name="delete_from_cart"),
    path('product_detail/<int:id>/', product_detail_view, name='product_detail'),
    path("checkout/<int:id>/", checkout, name="checkout"),
    path("payment_success/<int:id>/", payment_success, name="payment_success"),
    path("checkout_failed/", payment_failed, name="payment_failed"),
    path("track-order/", track_order, name="track_order"),
    path("all_orders/", all_orders_of_user, name="all_orders"),
    path('delete-order/<int:order_id>/', delete_order, name='delete_order'),
    path('add-review/<int:order_id>/', add_review, name='add_review'),
    path('product/<int:id>/', product_detail_view, name='product_detail'),
    path('add_product/', add_product, name='add_product'),
    path('create_store/', create_store, name='create_store'),
    path('store/<int:store_id>/products/', store_products, name="store_products"),
    path('cart_checkout/',cart_checkout,name="cart_checkout")
]