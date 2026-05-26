from django.contrib import admin
from django.utils.html import format_html
from .models import MainBanner


@admin.register(MainBanner)
class MainBannerAdmin(admin.ModelAdmin):
    list_display  = ['id', 'title', 'desktop_preview', 'mobile_preview', 'display_order', 'is_active']
    list_editable = ['display_order', 'is_active']
    ordering      = ['display_order']
    readonly_fields = ['desktop_preview', 'mobile_preview']

    fieldsets = (
        ('Images', {
            'fields': (
                ('image',        'desktop_preview'),
                ('mobile_image', 'mobile_preview'),
            ),
            'description': 'Upload a landscape image for desktop and an optional portrait image for mobile.',
        }),
        ('Content', {
            'fields': ('title', 'subtitle', 'cta_label', 'cta_url'),
        }),
        ('Visibility', {
            'fields': ('display_order', 'is_active'),
        }),
    )

    # ── Preview helpers ───────────────────────────────────────────────────

    @admin.display(description='Desktop Preview')
    def desktop_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="height:60px;border-radius:4px;'
                'object-fit:cover;border:1px solid #ddd;" />',
                obj.image.url,
            )
        return '—'

    @admin.display(description='Mobile Preview')
    def mobile_preview(self, obj):
        if obj.mobile_image:
            return format_html(
                '<img src="{}" style="height:60px;border-radius:4px;'
                'object-fit:cover;border:1px solid #ddd;" />',
                obj.mobile_image.url,
            )
        return format_html('<span style="color:#aaa;">uses desktop</span>')