from django.contrib import admin

from .models import Customer, Order, Store, Rates

admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(Store)
admin.site.register(Rates)