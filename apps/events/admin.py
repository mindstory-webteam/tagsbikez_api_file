from django.contrib import admin
from .models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display  = ['title', 'starting_point', 'destination', 'start_date', 'end_date', 'display_order', 'is_active']
    list_editable = ['display_order', 'is_active']
    list_filter   = ['is_active', 'start_date']
    search_fields = ['title', 'starting_point', 'destination']
    date_hierarchy = 'start_date'
    ordering      = ['start_date']
    fieldsets = (
        ('Event Info', {
            'fields': ('title', 'image', 'info_url'),
        }),
        ('Route', {
            'fields': ('starting_point', 'destination'),
        }),
        ('Dates', {
            'fields': ('start_date', 'end_date'),
        }),
        ('Visibility', {
            'fields': ('display_order', 'is_active'),
        }),
    )
