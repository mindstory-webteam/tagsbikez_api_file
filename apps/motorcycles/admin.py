"""
apps/motorcycles/admin.py
"""

from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import (
    MotorcycleProduct,
    ProductColor,
    ProductTopAbout,
    ProductFeatureSection,
)


class ProductTopAboutInline(admin.StackedInline):
    model               = ProductTopAbout
    extra               = 0
    max_num             = 1
    fields              = ('top_image', 'image_preview', 'heading', 'description')
    readonly_fields     = ('image_preview',)
    verbose_name        = 'Top About Section'
    verbose_name_plural = '① TOP ABOUT SECTION  (Image · Heading · Description)'

    @admin.display(description='Current Image')
    def image_preview(self, obj):
        if obj.pk and obj.top_image:
            return format_html(
                '<img src="{}" style="max-height:120px;border-radius:6px;'
                'object-fit:cover;border:1px solid #ddd;" />',
                obj.top_image.url,
            )
        return '— upload an image above —'


class ProductColorInline(admin.TabularInline):
    model               = ProductColor
    extra               = 1
    fields              = ('display_order', 'name', 'hex', 'color_swatch', 'image', 'price')
    readonly_fields     = ('color_swatch',)
    verbose_name        = 'Color Variant'
    verbose_name_plural = '② COLOR VARIANTS  (Name · Hex · Image · Price)'

    @admin.display(description='Swatch')
    def color_swatch(self, obj):
        if obj.hex:
            return format_html(
                '<span style="display:inline-block;width:28px;height:28px;'
                'border-radius:4px;background:{};border:1px solid #ccc;"></span>',
                obj.hex,
            )
        return '—'


class ProductFeatureSectionInline(admin.StackedInline):
    model               = ProductFeatureSection
    extra               = 1
    fields              = ('display_order', 'image', 'image_preview', 'title', 'description')
    readonly_fields     = ('image_preview',)
    verbose_name        = 'Feature / Story Section'
    verbose_name_plural = '③ BOTTOM FEATURE SECTIONS  (Image · Title · Description)'

    @admin.display(description='Preview')
    def image_preview(self, obj):
        if obj.pk and obj.image:
            return format_html(
                '<img src="{}" style="max-height:100px;border-radius:6px;'
                'object-fit:cover;border:1px solid #ddd;" />',
                obj.image.url,
            )
        return '— upload an image above —'


@admin.register(MotorcycleProduct)
class MotorcycleProductAdmin(admin.ModelAdmin):
    list_display  = [
        'name', 'category',
        'engine_cc', 'power', 'torque',
        'emi_starts_at', 'color_count',
        'coming_soon_badge', 'has_top_about', 'feature_count',
        'display_order', 'is_active',
    ]
    list_editable       = ['display_order', 'is_active']
    list_filter         = ['category', 'is_active', 'coming_soon']
    search_fields       = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    autocomplete_fields = ['category']

    # ── Bulk Import button injected into the changelist ────────────────────
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['bulk_import_url'] = '/admin/motorcycles/bulk-import/'
        extra_context['bulk_import_button'] = format_html(
            '<a href="{}" style="'
            'display:inline-block;margin-left:10px;padding:6px 14px;'
            'background:#2e7d32;color:#fff;border-radius:4px;font-size:13px;'
            'font-weight:600;text-decoration:none;vertical-align:middle;'
            'line-height:1.5;">'
            '📥 Bulk Import (Excel / CSV)'
            '</a>',
            '/admin/motorcycles/bulk-import/',
        )
        return super().changelist_view(request, extra_context=extra_context)

    def get_urls(self):
        from django.urls import path as dj_path
        from .bulk_import import bulk_import_view
        custom = [
            dj_path(
                "bulk-import/",
                self.admin_site.admin_view(bulk_import_view),
                name="motorcycles_motorcycleproduct_bulk_import",
            ),
        ]
        return custom + super().get_urls()

    fieldsets = (
        ('Basic Info', {
            'fields': (
                'category', 'name', 'slug',
                'featured_image', 'description',
            ),
        }),
        ('Specifications', {
            'description': 'All specification fields are optional.',
            'fields': ('engine_cc', 'power', 'torque'),
            'classes': ('collapse',),
        }),
        ('Pricing', {
            'fields': ('emi_starts_at',),
            'description': 'Shown on listing cards as "EMI STARTS @"',
        }),
        ('Brochure', {
            'fields': ('brochure_file',),
        }),
        ('Visibility', {
            'fields': ('coming_soon', 'display_order', 'is_active'),
        }),
    )

    inlines = [
        ProductTopAboutInline,
        ProductColorInline,
        ProductFeatureSectionInline,
    ]

    @admin.display(description='Colors')
    def color_count(self, obj):
        count = obj.colors.count()
        return f"{count} color{'s' if count != 1 else ''}"

    @admin.display(description='Top About', boolean=True)
    def has_top_about(self, obj):
        return hasattr(obj, 'top_about') and obj.top_about is not None

    @admin.display(description='Features')
    def feature_count(self, obj):
        count = obj.features.count()
        return f"{count} section{'s' if count != 1 else ''}"

    @admin.display(description='Status')
    def coming_soon_badge(self, obj):
        if obj.coming_soon:
            return format_html(
                '<span style="background:#e53e3e;color:#fff;padding:2px 8px;'
                'border-radius:4px;font-size:11px;font-weight:bold;">COMING SOON</span>'
            )
        return format_html(
            '<span style="background:#38a169;color:#fff;padding:2px 8px;'
            'border-radius:4px;font-size:11px;">LIVE</span>'
        )


@admin.register(ProductColor)
class ProductColorAdmin(admin.ModelAdmin):
    list_display  = ['motorcycle', 'name', 'color_swatch', 'price', 'display_order']
    list_editable = ['display_order']
    list_filter   = ['motorcycle__category']
    search_fields = ['name', 'motorcycle__name']
    raw_id_fields = ['motorcycle']

    @admin.display(description='Swatch')
    def color_swatch(self, obj):
        if obj.hex:
            return format_html(
                '<span style="display:inline-block;width:28px;height:28px;'
                'border-radius:4px;background:{};border:1px solid #ccc;"></span>',
                obj.hex,
            )
        return '—'


@admin.register(ProductTopAbout)
class ProductTopAboutAdmin(admin.ModelAdmin):
    list_display    = ['motorcycle', 'heading', 'image_preview']
    search_fields   = ['motorcycle__name', 'heading']
    raw_id_fields   = ['motorcycle']
    readonly_fields = ['image_preview']

    fieldsets = (
        (None, {
            'fields': ('motorcycle', 'top_image', 'image_preview', 'heading', 'description'),
        }),
    )

    @admin.display(description='Image Preview')
    def image_preview(self, obj):
        if obj.top_image:
            return format_html(
                '<img src="{}" style="max-height:100px;border-radius:6px;'
                'object-fit:cover;border:1px solid #ddd;" />',
                obj.top_image.url,
            )
        return '—'


@admin.register(ProductFeatureSection)
class ProductFeatureSectionAdmin(admin.ModelAdmin):
    list_display    = ['motorcycle', 'title', 'image_preview', 'display_order']
    list_editable   = ['display_order']
    list_filter     = ['motorcycle__category']
    search_fields   = ['title', 'motorcycle__name']
    raw_id_fields   = ['motorcycle']
    readonly_fields = ['image_preview']

    fieldsets = (
        (None, {
            'fields': ('motorcycle', 'display_order', 'image', 'image_preview', 'title', 'description'),
        }),
    )

    @admin.display(description='Image Preview')
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height:100px;border-radius:6px;'
                'object-fit:cover;border:1px solid #ddd;" />',
                obj.image.url,
            )
        return '—'