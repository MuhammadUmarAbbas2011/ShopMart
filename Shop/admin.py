from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Products)
admin.site.register(Stores)
admin.site.register(CheckoutModel)
admin.site.register(OrderModel)