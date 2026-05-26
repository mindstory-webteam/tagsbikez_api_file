"""
apps/careers/admin.py
"""

from django.contrib import admin
from django.utils.html import format_html
from .models import CareerDepartment, CareerRole


class CareerRoleInline(admin.TabularInline):
    model   = CareerRole
    extra   = 1
    fields  = ('display_order', 'title', 'whatsapp_number', 'whatsapp_message', 'is_active', 'whatsapp_preview')
    readonly_fields = ('whatsapp_preview',)

    @admin.display(description='WhatsApp Link Preview')
    def whatsapp_preview(self, obj):
        if obj.pk:
            url = obj.get_whatsapp_url()
            return format_html(
                '<a href="{}" target="_blank" style="color:#25D366;font-weight:bold;">▶ Test Link</a>',
                url,
            )
        return '—'


@admin.register(CareerDepartment)
class CareerDepartmentAdmin(admin.ModelAdmin):
    list_display  = ['name', 'icon', 'role_count', 'display_order', 'is_active']
    list_editable = ['display_order', 'is_active']
    search_fields = ['name']
    inlines       = [CareerRoleInline]

    @admin.display(description='Roles')
    def role_count(self, obj):
        count = obj.roles.count()
        return f"{count} role{'s' if count != 1 else ''}"


@admin.register(CareerRole)
class CareerRoleAdmin(admin.ModelAdmin):
    list_display   = ['title', 'department', 'whatsapp_number', 'whatsapp_link', 'display_order', 'is_active']
    list_editable  = ['display_order', 'is_active']
    list_filter    = ['department', 'is_active']
    search_fields  = ['title', 'department__name']
    raw_id_fields  = ['department']

    @admin.display(description='WhatsApp')
    def whatsapp_link(self, obj):
        url = obj.get_whatsapp_url()
        return format_html(
            '<a href="{}" target="_blank" style="color:#25D366;font-weight:bold;">▶ Open</a>',
            url,
        )