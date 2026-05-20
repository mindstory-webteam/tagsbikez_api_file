from django.contrib import admin
from .models import ProductCategory


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display        = ['name', 'slug', 'display_order', 'is_active']
    list_editable       = ['display_order', 'is_active']
    prepopulated_fields = {'slug': ('name',)}
    search_fields       = ['name', 'slug']