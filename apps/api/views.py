"""
apps/api/views.py

All API views for TagsBikez — filters wired on every endpoint.

Endpoints:
  GET  /api/banners/                → MainBannerListView
  GET  /api/events/                 → EventListView
  GET  /api/events/upcoming/        → UpcomingEventListView
  GET  /api/gallery/                → GalleryImageListView
  GET  /api/categories/             → ProductCategoryListView
  GET  /api/categories/<slug>/      → ProductCategoryDetailView
  GET  /api/motorcycles/            → MotorcycleProductListView
  GET  /api/motorcycles/<slug>/     → MotorcycleProductDetailView

Query-param filters available per endpoint
──────────────────────────────────────────
  /api/banners/
      ?is_active=true

  /api/events/
      ?is_active=true
      ?destination=kochi          (case-insensitive contains)
      ?starting_point=thrissur    (case-insensitive contains)
      ?start_date=2025-01-01      (events starting on or after)
      ?end_date=2025-12-31        (events ending on or before)
      ?upcoming=true              (end_date >= today)

  /api/gallery/
      ?is_active=true

  /api/categories/
      ?is_active=true
      ?name=street                (case-insensitive contains)

  /api/motorcycles/
      ?category=street            (exact category slug)
      ?is_active=true

NO /api/colors/ — colors are nested inside /api/motorcycles/<slug>/
"""

from django.utils import timezone

from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny

from django_filters.rest_framework import DjangoFilterBackend

from apps.home.models import MainBanner
from apps.events.models import Event
from apps.gallery.models import GalleryImage
from apps.categories.models import ProductCategory
from apps.motorcycles.models import MotorcycleProduct

from .serializers import (
    MainBannerSerializer,
    EventSerializer,
    GalleryImageSerializer,
    ProductCategoryListSerializer,
    ProductCategoryDetailSerializer,
    MotorcycleProductListSerializer,
    MotorcycleProductDetailSerializer,
)
from .filters import (
    MainBannerFilter,
    EventFilter,
    GalleryImageFilter,
    ProductCategoryFilter,
    MotorcycleProductFilter,
)


# ─────────────────────────────────────────────────────────────────────────────
# HOME — MAIN BANNER
# ─────────────────────────────────────────────────────────────────────────────

class MainBannerListView(ListAPIView):
    """
    GET /api/banners/
    Query params: ?is_active=true
    """
    serializer_class   = MainBannerSerializer
    permission_classes = [AllowAny]
    filter_backends    = [DjangoFilterBackend]
    filterset_class    = MainBannerFilter

    def get_queryset(self):
        return (
            MainBanner.objects
            .filter(is_active=True)
            .order_by('display_order')
        )


# ─────────────────────────────────────────────────────────────────────────────
# EVENTS
# ─────────────────────────────────────────────────────────────────────────────

class EventListView(ListAPIView):
    """
    GET /api/events/
    Query params: ?is_active ?destination ?starting_point ?start_date ?end_date ?upcoming
    """
    serializer_class   = EventSerializer
    permission_classes = [AllowAny]
    filter_backends    = [DjangoFilterBackend]
    filterset_class    = EventFilter

    def get_queryset(self):
        return (
            Event.objects
            .filter(is_active=True)
            .order_by('display_order', 'start_date')
        )


class UpcomingEventListView(ListAPIView):
    """
    GET /api/events/upcoming/
    Hardcoded to end_date >= today. Also accepts all EventFilter params.
    """
    serializer_class   = EventSerializer
    permission_classes = [AllowAny]
    filter_backends    = [DjangoFilterBackend]
    filterset_class    = EventFilter

    def get_queryset(self):
        today = timezone.now().date()
        return (
            Event.objects
            .filter(is_active=True, end_date__gte=today)
            .order_by('display_order', 'start_date')
        )


# ─────────────────────────────────────────────────────────────────────────────
# GALLERY
# ─────────────────────────────────────────────────────────────────────────────

class GalleryImageListView(ListAPIView):
    """
    GET /api/gallery/
    Query params: ?is_active=true
    """
    serializer_class   = GalleryImageSerializer
    permission_classes = [AllowAny]
    filter_backends    = [DjangoFilterBackend]
    filterset_class    = GalleryImageFilter

    def get_queryset(self):
        return (
            GalleryImage.objects
            .filter(is_active=True)
            .order_by('display_order')
        )


# ─────────────────────────────────────────────────────────────────────────────
# CATEGORIES
# ─────────────────────────────────────────────────────────────────────────────

class ProductCategoryListView(ListAPIView):
    """
    GET /api/categories/
    Query params: ?is_active=true  ?name=street
    """
    serializer_class   = ProductCategoryListSerializer
    permission_classes = [AllowAny]
    filter_backends    = [DjangoFilterBackend]
    filterset_class    = ProductCategoryFilter

    def get_queryset(self):
        return (
            ProductCategory.objects
            .filter(is_active=True)
            .order_by('display_order', 'name')
        )


class ProductCategoryDetailView(RetrieveAPIView):
    """
    GET /api/categories/<slug>/
    No filters needed on single-object detail.
    """
    serializer_class   = ProductCategoryDetailSerializer
    permission_classes = [AllowAny]
    lookup_field       = 'slug'

    def get_queryset(self):
        return ProductCategory.objects.filter(is_active=True)


# ─────────────────────────────────────────────────────────────────────────────
# MOTORCYCLES — colors nested, no /api/colors/ endpoint
# ─────────────────────────────────────────────────────────────────────────────

def _motorcycle_qs():
    """
    Shared optimised queryset.
      select_related   → category, top_about   (no extra JOIN queries)
      prefetch_related → colors, features      (2 bulk queries, no N+1)
    """
    return (
        MotorcycleProduct.objects
        .filter(is_active=True)
        .select_related('category', 'top_about')
        .prefetch_related('colors', 'features')
        .order_by('display_order', 'name')
    )


class MotorcycleProductListView(ListAPIView):
    """
    GET /api/motorcycles/
    Query params: ?category=street  ?is_active=true

    base_price = price of lowest display_order color variant.
    Colors are NOT expanded here — use /api/motorcycles/<slug>/ for full detail.
    """
    serializer_class   = MotorcycleProductListSerializer
    permission_classes = [AllowAny]
    filter_backends    = [DjangoFilterBackend]
    filterset_class    = MotorcycleProductFilter

    def get_queryset(self):
        return _motorcycle_qs()


class MotorcycleProductDetailView(RetrieveAPIView):
    """
    GET /api/motorcycles/<slug>/
    Full detail — top_about + colors + features all nested.
    No filters on detail (lookup by slug).
    """
    serializer_class   = MotorcycleProductDetailSerializer
    permission_classes = [AllowAny]
    lookup_field       = 'slug'

    def get_queryset(self):
        return _motorcycle_qs()