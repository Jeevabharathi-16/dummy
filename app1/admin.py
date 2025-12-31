from django.contrib import admin
from .models import *
# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display=['ch']

class ProductsAdmin(admin.ModelAdmin):
    list_display=['p_name','p_price','category']


admin.site.register(Category,CategoryAdmin)

admin.site.register(Product,ProductsAdmin)