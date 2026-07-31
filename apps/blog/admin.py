"""
apps/blog/admin.py
"""

from django.contrib import admin
from django.utils.html import format_html
from .models import BlogPost, BlogParagraph


class BlogParagraphInline(admin.TabularInline):
    model  = BlogParagraph
    extra  = 1
    fields = ('display_order', 'text')
    ordering = ('display_order', 'id')


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display  = [
        'thumb', 'title', 'author', 'published_date',
        'popular', 'para_count', 'display_order', 'is_active',
    ]
    list_display_links  = ['title']
    list_editable       = ['popular', 'display_order', 'is_active']
    list_filter         = ['is_active', 'popular', 'published_date', 'author']
    search_fields       = ['title', 'excerpt', 'author', 'paragraphs__text']
    date_hierarchy      = 'published_date'
    ordering            = ['-published_date', 'display_order']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields     = ['thumb_large', 'og_image_preview', 'created_at', 'updated_at']
    inlines             = [BlogParagraphInline]

    fieldsets = (
        ('Headline', {
            'fields': ('title', 'slug', 'author', 'published_date'),
        }),
        ('Card / Sidebar', {
            'fields': ('image', 'thumb_large', 'excerpt', 'popular'),
            'description': 'Shown on the BLOGS listing cards and the POPULAR sidebar.',
        }),
        ('SEO', {
            'fields': (
                'meta_title', 'meta_description', 'meta_keywords',
                'og_image', 'og_image_preview',
                'canonical_url', 'noindex',
            ),
            'description': 'Controls how this post appears in Google search results and '
                            'when shared on social media. Leave blank to fall back to the '
                            'title / excerpt / main image above.',
        }),
        ('Visibility', {
            'fields': ('display_order', 'is_active', 'created_at', 'updated_at'),
        }),
    )

    @admin.display(description='')
    def thumb(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width:54px;height:38px;object-fit:cover;'
                'border-radius:4px;" />',
                obj.image.url,
            )
        return '-'

    @admin.display(description='Preview')
    def thumb_large(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-width:320px;border-radius:8px;" />',
                obj.image.url,
            )
        return '-'

    @admin.display(description='Paras')
    def para_count(self, obj):
        return obj.paragraphs.count()

    @admin.display(description='Social share preview')
    def og_image_preview(self, obj):
        if obj.og_image:
            return format_html(
                '<img src="{}" style="max-width:320px;border-radius:8px;" />',
                obj.og_image.url,
            )
        return 'No custom social image set — the main post image above will be used instead.'