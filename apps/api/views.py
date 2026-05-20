"""
apps/api/views.py
All DRF ViewSets.
About section removed. Home / Events / Gallery added.
"""

"""
apps/api/views.py
"""

from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend

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

from .serializers import (
    MainBannerSerializer,
    EventSerializer,
    GalleryImageSerializer,
    ProductCategoryListSerializer,
    ProductCategoryDetailSerializer,
    MotorcycleProductListSerializer,
    MotorcycleProductDetailSerializer,
    ProductColorSerializer,
    ProductTopAboutSerializer,
    ProductFeatureSectionSerializer,
)
from .filters import (
    MainBannerFilter,
    EventFilter,
    GalleryImageFilter,
    ProductCategoryFilter,
    MotorcycleProductFilter,
    ProductColorFilter,
    ProductTopAboutFilter,
    ProductFeatureSectionFilter,
)
from .pagination import StandardResultsPagination


class MainBannerViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = MainBannerSerializer
    filter_backends  = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class  = MainBannerFilter
    ordering_fields  = ['display_order']
    ordering         = ['display_order']
    pagination_class = StandardResultsPagination

    def get_queryset(self):
        return MainBanner.objects.filter(is_active=True)


class EventViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = EventSerializer
    filter_backends  = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_class  = EventFilter
    ordering_fields  = ['start_date', 'display_order']
    ordering         = ['start_date']
    search_fields    = ['title', 'starting_point', 'destination']
    pagination_class = StandardResultsPagination

    def get_queryset(self):
        return Event.objects.filter(is_active=True)


class GalleryImageViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = GalleryImageSerializer
    filter_backends  = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class  = GalleryImageFilter
    ordering_fields  = ['display_order', 'uploaded_at']
    ordering         = ['display_order']
    pagination_class = StandardResultsPagination

    def get_queryset(self):
        return GalleryImage.objects.filter(is_active=True)


class ProductCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    lookup_field     = 'slug'
    serializer_class = ProductCategoryListSerializer
    filter_backends  = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class  = ProductCategoryFilter
    ordering_fields  = ['display_order', 'name']
    ordering         = ['display_order']
    pagination_class = StandardResultsPagination

    def get_queryset(self):
        return ProductCategory.objects.filter(is_active=True)


class MotorcycleProductViewSet(viewsets.ReadOnlyModelViewSet):
    lookup_field     = 'slug'
    filter_backends  = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class  = MotorcycleProductFilter
    ordering_fields  = ['display_order', 'name', 'created_at']
    ordering         = ['display_order']
    pagination_class = StandardResultsPagination

    def get_queryset(self):
        return (
            MotorcycleProduct.objects
            .filter(is_active=True)
            .select_related('category', 'top_about')
            .prefetch_related('colors', 'features')
        )

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return MotorcycleProductDetailSerializer
        return MotorcycleProductListSerializer


class ProductColorViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ProductColorSerializer
    filter_backends  = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class  = ProductColorFilter
    ordering_fields  = ['display_order']
    ordering         = ['display_order']
    pagination_class = StandardResultsPagination

    def get_queryset(self):
        return ProductColor.objects.select_related('motorcycle').all()


class ProductTopAboutViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ProductTopAboutSerializer
    filter_backends  = [DjangoFilterBackend]
    filterset_class  = ProductTopAboutFilter
    pagination_class = StandardResultsPagination

    def get_queryset(self):
        return ProductTopAbout.objects.select_related('motorcycle').all()


class ProductFeatureSectionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ProductFeatureSectionSerializer
    filter_backends  = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class  = ProductFeatureSectionFilter
    ordering_fields  = ['display_order']
    ordering         = ['display_order']
    pagination_class = StandardResultsPagination

    def get_queryset(self):
        return ProductFeatureSection.objects.select_related('motorcycle').all()
