"""
apps/api/filters.py
django-filter FilterSet classes.
"""
# -------------------------------------------------------------------

"""
apps/api/filters.py
"""

import django_filters
from apps.categories.models import ProductCategory
from apps.motorcycles.models import (
    MotorcycleProduct,
    ProductColor,
    ProductTopAbout,
    ProductFeatureSection,
)
from apps.home.models import MainBanner
from apps.events.models import Event
from apps.gallery.models import GalleryImage

# ── Home ─────────────────────────────────────────────────────────────────────
class MainBannerFilter(django_filters.FilterSet):
    is_active = django_filters.BooleanFilter(field_name='is_active')

    class Meta:
        model  = MainBanner
        fields = ['is_active']

# ── Events ───────────────────────────────────────────────────────────────────

class EventFilter(django_filters.FilterSet):
    is_active      = django_filters.BooleanFilter(field_name='is_active')
    destination    = django_filters.CharFilter(field_name='destination',    lookup_expr='icontains')
    starting_point = django_filters.CharFilter(field_name='starting_point', lookup_expr='icontains')
    start_date     = django_filters.DateFilter(field_name='start_date',     lookup_expr='gte')
    end_date       = django_filters.DateFilter(field_name='end_date',       lookup_expr='lte')
    upcoming       = django_filters.BooleanFilter(method='filter_upcoming')

    class Meta:
        model  = Event
        fields = ['is_active', 'destination', 'starting_point', 'start_date', 'end_date']

    def filter_upcoming(self, queryset, name, value):
        from django.utils import timezone
        today = timezone.now().date()
        if value:
            return queryset.filter(end_date__gte=today)
        return queryset.filter(end_date__lt=today)

# ── Gallery ──────────────────────────────────────────────────────────────────

class GalleryImageFilter(django_filters.FilterSet):
    is_active = django_filters.BooleanFilter(field_name='is_active')

    class Meta:
        model  = GalleryImage
        fields = ['is_active']

# ── Categories ───────────────────────────────────────────────────────────────

class ProductCategoryFilter(django_filters.FilterSet):
    is_active = django_filters.BooleanFilter(field_name='is_active')
    name      = django_filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model  = ProductCategory
        fields = ['is_active', 'name']

# ── Motorcycles ──────────────────────────────────────────────────────────────

class MotorcycleProductFilter(django_filters.FilterSet):
    category  = django_filters.CharFilter(field_name='category__slug', lookup_expr='exact')
    is_active = django_filters.BooleanFilter(field_name='is_active')

    class Meta:
        model  = MotorcycleProduct
        fields = ['category', 'is_active']


class ProductColorFilter(django_filters.FilterSet):
    motorcycle = django_filters.CharFilter(field_name='motorcycle__slug', lookup_expr='exact')

    class Meta:
        model  = ProductColor
        fields = ['motorcycle']


class ProductTopAboutFilter(django_filters.FilterSet):
    motorcycle = django_filters.CharFilter(field_name='motorcycle__slug', lookup_expr='exact')

    class Meta:
        model  = ProductTopAbout
        fields = ['motorcycle']


class ProductFeatureSectionFilter(django_filters.FilterSet):
    motorcycle = django_filters.CharFilter(field_name='motorcycle__slug', lookup_expr='exact')

    class Meta:
        model  = ProductFeatureSection
        fields = ['motorcycle']