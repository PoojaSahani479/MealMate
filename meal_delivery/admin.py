from django.contrib import admin

from .models import Customers, Restaurants

# Register your models here.
admin.site.register(Customers)
admin.site.register(Restaurants)
