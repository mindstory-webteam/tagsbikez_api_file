from django.contrib import admin
from .models import MainBanner


@admin.register(MainBanner)
class MainBannerAdmin(admin.ModelAdmin):
    list_display  = ['id', 'title', 'display_order', 'is_active']
    list_editable = ['display_order', 'is_active']
    ordering      = ['display_order']
