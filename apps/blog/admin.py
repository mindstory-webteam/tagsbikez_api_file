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
    readonly_fields     = ['thumb_large', 'created_at', 'updated_at']
    inlines             = [BlogParagraphInline]

    fieldsets = (
        ('Headline', {
            'fields': ('title', 'slug', 'author', 'published_date'),
        }),
        ('Card / Sidebar', {
            'fields': ('image', 'thumb_large', 'excerpt', 'popular'),
            'description': 'Shown on the BLOGS listing cards and the POPULAR sidebar.',
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
