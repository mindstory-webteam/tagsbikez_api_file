from django.contrib import admin
from .models import GalleryImage


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display  = ['id', 'caption', 'display_order', 'is_active', 'uploaded_at']
    list_editable = ['display_order', 'is_active']
    search_fields = ['caption']
    ordering      = ['display_order']