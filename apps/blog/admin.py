"""
apps/blog/admin.py
"""

from django.contrib import admin
from django.utils.html import format_html
from .models import BlogPost


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display  = [
        'thumb', 'title', 'author', 'published_date',
        'is_popular', 'display_order', 'is_active',
    ]
    list_display_links = ['title']
    list_editable      = ['is_popular', 'display_order', 'is_active']
    list_filter        = ['is_active', 'is_popular', 'published_date', 'author']
    search_fields      = ['title', 'excerpt', 'body', 'author']
    date_hierarchy     = 'published_date'
    ordering           = ['-published_date', 'display_order']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields     = ['thumb_large', 'created_at', 'updated_at']

    fieldsets = (
        ('Headline', {
            'fields': ('title', 'slug', 'author', 'published_date'),
        }),
        ('Card / Sidebar', {
            'fields': ('featured_image', 'thumb_large', 'excerpt', 'is_popular'),
            'description': 'Shown on the BLOGS listing cards and the POPULAR sidebar.',
        }),
        ('Detail page — top', {
            'fields': ('intro', 'highlight'),
            'description': '“intro” is the lead paragraph. “highlight” is the big RED sub-heading.',
        }),
        ('Detail page — body', {
            'fields': ('body_image', 'body_image_caption', 'body'),
            'description': 'The body field accepts HTML and is rendered as the inner-page article body.',
        }),
        ('SEO', {
            'fields': ('meta_description',),
            'classes': ('collapse',),
        }),
        ('Visibility', {
            'fields': ('display_order', 'is_active', 'created_at', 'updated_at'),
        }),
    )

    @admin.display(description='')
    def thumb(self, obj):
        if obj.featured_image:
            return format_html(
                '<img src="{}" style="width:54px;height:38px;object-fit:cover;'
                'border-radius:4px;" />',
                obj.featured_image.url,
            )
        return '—'

    @admin.display(description='Preview')
    def thumb_large(self, obj):
        if obj.featured_image:
            return format_html(
                '<img src="{}" style="max-width:320px;border-radius:8px;" />',
                obj.featured_image.url,
            )
        return '—'
