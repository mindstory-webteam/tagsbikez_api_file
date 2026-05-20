"""
apps/motorcycles/admin.py

Admin registrations for MotorcycleProduct and its related models.

Layout mirrors the Product Model Page spec:
  ┌─ MotorcycleProductAdmin ──────────────────────────┐
  │  ProductTopAboutInline      (top hero section)    │
  │  ProductColorInline         (color variants)      │
  │  ProductFeatureSectionInline (bottom stories)     │
  └───────────────────────────────────────────────────┘
"""

from django.contrib import admin
from django.utils.html import format_html
from .models import (
    MotorcycleProduct,
    ProductColor,
    ProductTopAbout,
    ProductFeatureSection,
)


# ─────────────────────────────────────────────────────────────────────────────
# INLINES
# ─────────────────────────────────────────────────────────────────────────────

class ProductTopAboutInline(admin.StackedInline):
    """
    TOP ABOUT SECTION — Image / Heading / Description
    One per motorcycle, so StackedInline with max_num=1.
    """
    model   = ProductTopAbout
    extra   = 0
    max_num = 1
    fields  = ('top_image', 'heading', 'description')
    verbose_name        = 'Top About Section'
    verbose_name_plural = 'Top About Section (Image · Heading · Description)'


class ProductColorInline(admin.TabularInline):
    """
    COLOR VARIANTS — name / hex swatch / image / price
    """
    model  = ProductColor
    extra  = 1
    fields = ('display_order', 'name', 'hex', 'color_swatch', 'image', 'price')
    readonly_fields = ('color_swatch',)

    @admin.display(description='Swatch')
    def color_swatch(self, obj):
        if obj.hex:
            return format_html(
                '<span style="display:inline-block;width:24px;height:24px;'
                'border-radius:4px;background:{};border:1px solid #ccc;"></span>',
                obj.hex
            )
        return '—'


class ProductFeatureSectionInline(admin.TabularInline):
    """
    BOTTOM FEATURE SECTIONS — Image / Title / Description
    """
    model  = ProductFeatureSection
    extra  = 1
    fields = ('display_order', 'title', 'description', 'image')
    verbose_name        = 'Feature / Story Section'
    verbose_name_plural = 'Bottom Feature Sections (Image · Title · Description)'


# ─────────────────────────────────────────────────────────────────────────────
# MAIN ADMIN
# ─────────────────────────────────────────────────────────────────────────────

@admin.register(MotorcycleProduct)
class MotorcycleProductAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'category', 'engine_cc', 'power', 'torque',
        'color_count', 'display_order', 'is_active',
    ]
    list_editable  = ['display_order', 'is_active']
    list_filter    = ['category', 'is_active']
    search_fields  = ['name', 'slug', 'short_description']
    prepopulated_fields = {'slug': ('name',)}
    autocomplete_fields = ['category']

    fieldsets = (
        ('Basic Info', {
            'fields': ('category', 'name', 'slug', 'featured_image',
                       'short_description', 'description'),
        }),
        ('Specifications', {
            'fields': ('engine_cc', 'power', 'torque'),
        }),
        ('Brochure', {
            'fields': ('brochure_file',),
        }),
        ('Visibility', {
            'fields': ('display_order', 'is_active'),
        }),
    )

    inlines = [
        ProductTopAboutInline,       # Top: Image / Heading / Description
        ProductColorInline,          # Detail: Color variants with price
        ProductFeatureSectionInline, # Bottom: Image / Title / Description
    ]

    @admin.display(description='Colors')
    def color_count(self, obj):
        count = obj.colors.count()
        return f"{count} color{'s' if count != 1 else ''}"


# ─────────────────────────────────────────────────────────────────────────────
# STANDALONE ADMINS (for quick access / bulk editing)
# ─────────────────────────────────────────────────────────────────────────────

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
                '<span style="display:inline-block;width:24px;height:24px;'
                'border-radius:4px;background:{};border:1px solid #ccc;"></span>',
                obj.hex
            )
        return '—'


@admin.register(ProductTopAbout)
class ProductTopAboutAdmin(admin.ModelAdmin):
    list_display  = ['motorcycle', 'heading']
    search_fields = ['motorcycle__name', 'heading']
    raw_id_fields = ['motorcycle']


@admin.register(ProductFeatureSection)
class ProductFeatureSectionAdmin(admin.ModelAdmin):
    list_display  = ['motorcycle', 'title', 'display_order']
    list_editable = ['display_order']
    list_filter   = ['motorcycle__category']
    search_fields = ['title', 'motorcycle__name']
    raw_id_fields = ['motorcycle']
