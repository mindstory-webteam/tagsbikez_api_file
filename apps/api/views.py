"""
apps/api/views.py

All API views for TagsBikez.

Endpoints:
  GET  /api/banners/                → MainBannerListView
  GET  /api/events/                 → EventListView
  GET  /api/events/upcoming/        → UpcomingEventListView
  GET  /api/gallery/                → GalleryImageListView
  GET  /api/categories/             → ProductCategoryListView
  GET  /api/categories/<slug>/      → ProductCategoryDetailView
  GET  /api/motorcycles/            → MotorcycleProductListView
  GET  /api/motorcycles/<slug>/     → MotorcycleProductDetailView
  GET  /api/careers/                → CareerDepartmentListView
"""

from django.utils import timezone

from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny
from rest_framework.filters import SearchFilter, OrderingFilter

from django_filters.rest_framework import DjangoFilterBackend

from apps.home.models import MainBanner
from apps.events.models import Event
from apps.gallery.models import GalleryImage
from apps.categories.models import ProductCategory
from apps.motorcycles.models import MotorcycleProduct
from apps.careers.models import CareerDepartment
from apps.blog.models import BlogPost

from .serializers import (
    MainBannerSerializer,
    EventSerializer,
    GalleryImageSerializer,
    ProductCategoryListSerializer,
    ProductCategoryDetailSerializer,
    MotorcycleProductListSerializer,
    MotorcycleProductDetailSerializer,
    CareerDepartmentSerializer,
    BlogPostCardSerializer,
    BlogPostDetailSerializer,
)
from .filters import (
    MainBannerFilter,
    EventFilter,
    GalleryImageFilter,
    ProductCategoryFilter,
    MotorcycleProductFilter,
    CareerDepartmentFilter,
    BlogPostFilter,
)


# ─────────────────────────────────────────────────────────────────────────────
# HOME — MAIN BANNER
# ─────────────────────────────────────────────────────────────────────────────

class MainBannerListView(ListAPIView):
    """GET /api/banners/  — ?is_active=true"""
    serializer_class   = MainBannerSerializer
    permission_classes = [AllowAny]
    filter_backends    = [DjangoFilterBackend]
    filterset_class    = MainBannerFilter

    def get_queryset(self):
        return MainBanner.objects.filter(is_active=True).order_by('display_order')


# ─────────────────────────────────────────────────────────────────────────────
# EVENTS
# ─────────────────────────────────────────────────────────────────────────────

class EventListView(ListAPIView):
    """GET /api/events/  — ?is_active ?destination ?starting_point ?start_date ?end_date ?upcoming"""
    serializer_class   = EventSerializer
    permission_classes = [AllowAny]
    filter_backends    = [DjangoFilterBackend]
    filterset_class    = EventFilter

    def get_queryset(self):
        return Event.objects.filter(is_active=True).order_by('display_order', 'start_date')


class UpcomingEventListView(ListAPIView):
    """GET /api/events/upcoming/  — end_date >= today"""
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
    """GET /api/gallery/  — ?is_active=true"""
    serializer_class   = GalleryImageSerializer
    permission_classes = [AllowAny]
    filter_backends    = [DjangoFilterBackend]
    filterset_class    = GalleryImageFilter

    def get_queryset(self):
        return GalleryImage.objects.filter(is_active=True).order_by('display_order')


# ─────────────────────────────────────────────────────────────────────────────
# CATEGORIES
# ─────────────────────────────────────────────────────────────────────────────

class ProductCategoryListView(ListAPIView):
    """GET /api/categories/  — ?is_active=true ?name=street"""
    serializer_class   = ProductCategoryListSerializer
    permission_classes = [AllowAny]
    filter_backends    = [DjangoFilterBackend]
    filterset_class    = ProductCategoryFilter

    def get_queryset(self):
        return ProductCategory.objects.filter(is_active=True).order_by('display_order', 'name')


class ProductCategoryDetailView(RetrieveAPIView):
    """GET /api/categories/<slug>/"""
    serializer_class   = ProductCategoryDetailSerializer
    permission_classes = [AllowAny]
    lookup_field       = 'slug'

    def get_queryset(self):
        return ProductCategory.objects.filter(is_active=True)


# ─────────────────────────────────────────────────────────────────────────────
# MOTORCYCLES
# ─────────────────────────────────────────────────────────────────────────────

def _motorcycle_qs():
    return (
        MotorcycleProduct.objects
        .filter(is_active=True)
        .select_related('category', 'top_about')
        .prefetch_related('colors', 'features')
        .order_by('display_order', 'name')
    )


class MotorcycleProductListView(ListAPIView):
    """GET /api/motorcycles/  — ?category=street ?is_active=true"""
    serializer_class   = MotorcycleProductListSerializer
    permission_classes = [AllowAny]
    filter_backends    = [DjangoFilterBackend]
    filterset_class    = MotorcycleProductFilter

    def get_queryset(self):
        return _motorcycle_qs()


class MotorcycleProductDetailView(RetrieveAPIView):
    """GET /api/motorcycles/<slug>/"""
    serializer_class   = MotorcycleProductDetailSerializer
    permission_classes = [AllowAny]
    lookup_field       = 'slug'

    def get_queryset(self):
        return _motorcycle_qs()


# ─────────────────────────────────────────────────────────────────────────────
# CAREERS
# ─────────────────────────────────────────────────────────────────────────────

class CareerDepartmentListView(ListAPIView):
    """
    GET /api/careers/
    Returns all active departments with roles nested inside.
    Each role includes whatsapp_url for the APPLY NOW button.

    Query params: ?is_active=true  ?name=sales
    """
    serializer_class   = CareerDepartmentSerializer
    permission_classes = [AllowAny]
    filter_backends    = [DjangoFilterBackend]
    filterset_class    = CareerDepartmentFilter

    def get_queryset(self):
        return (
            CareerDepartment.objects
            .filter(is_active=True)
            .prefetch_related('roles')
            .order_by('display_order', 'name')
        )

# ─────────────────────────────────────────────────────────────────────────────
# BLOG
# ─────────────────────────────────────────────────────────────────────────────

def _blog_qs():
    return BlogPost.objects.filter(is_active=True).order_by(
        '-published_date', 'display_order', '-id'
    )


class BlogPostListView(ListAPIView):
    """
    GET /api/blog/
    Paginated listing for the BLOGS grid.

    Query params:
      ?is_popular=true   ?author=admin   ?title=hunter
      ?search=hunter     (matches title / excerpt / body)
      ?ordering=published_date | -published_date | display_order
      ?page=1            ?page_size=12
    """
    serializer_class   = BlogPostCardSerializer
    permission_classes = [AllowAny]
    filter_backends    = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]
    filterset_class    = BlogPostFilter
    search_fields      = ['title', 'excerpt', 'body', 'author']
    ordering_fields    = ['published_date', 'display_order', 'created_at']

    def get_queryset(self):
        return _blog_qs()


class PopularBlogPostListView(ListAPIView):
    """
    GET /api/blog/popular/
    Posts flagged is_popular=True — drives the POPULAR sidebar.
    Not paginated (small, fixed list).
    """
    serializer_class   = BlogPostCardSerializer
    permission_classes = [AllowAny]
    pagination_class   = None

    def get_queryset(self):
        return _blog_qs().filter(is_popular=True)


class BlogPostDetailView(RetrieveAPIView):
    """
    GET /api/blog/<slug>/
    Full inner page incl. HTML body + previous/next neighbours.
    """
    serializer_class   = BlogPostDetailSerializer
    permission_classes = [AllowAny]
    lookup_field       = 'slug'

    def get_queryset(self):
        return BlogPost.objects.filter(is_active=True)
