from django.contrib import admin
from .models import Client, Product, Invoice, InvoiceItem, ActivityLog, Payment

# Register your models here.
admin.site.register(Client)
admin.site.register(Product)
admin.site.register(Invoice)
admin.site.register(InvoiceItem)
admin.site.register(ActivityLog)
admin.site.register(Payment)