from django.contrib import admin

from .models import Product, ProductInfo


class ProductAdmin(admin.ModelAdmin):
    list_display = ('url', 'datetime_add')
    search_fields = ('url', 'datetime_add')
    ordering = ('-datetime_add',)

class ProductInfoAdmin(admin.ModelAdmin):
    list_display = ('product', 'name', 'price', 'stock', 'datetime_scan')
    search_fields = ('product', 'name', 'price', 'stock', 'datetime_scan')
    ordering = ('-datetime_scan',)

admin.site.register(Product, ProductAdmin)
admin.site.register(ProductInfo, ProductInfoAdmin)