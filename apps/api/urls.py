"""
apps/api/urls.py

URL map (About removed, Home / Events / Gallery added):

  HOME
    /api/banners/                    list / detail

  EVENTS
    /api/events/                     list / detail

  GALLERY
    /api/gallery/                    list / detail (by slug)
    /api/gallery-images/             list / detail (?album=<slug>)

  CATEGORIES
    /api/categories/                 list / detail (by slug)

  MOTORCYCLES
    /api/motorcycles/                list / detail (by slug)
    /api/colors/                     list / detail (?motorcycle=<slug>)
    /api/top-about/                  list / detail (?motorcycle=<slug>)
    /api/features/                   list / detail (?motorcycle=<slug>)
"""

"""
apps/api/urls.py

  /api/banners/        — home banner slides
  /api/events/         — upcoming events
  /api/gallery/        — gallery images
  /api/categories/     — product categories
  /api/motorcycles/    — motorcycle products
  /api/colors/         — color variants
  /api/top-about/      — product top about sections
  /api/features/       — product feature sections
"""

from rest_framework.routers import DefaultRouter
from .views import (
    MainBannerViewSet,
    EventViewSet,
    GalleryImageViewSet,
    ProductCategoryViewSet,
    MotorcycleProductViewSet,
    ProductColorViewSet,
    ProductTopAboutViewSet,
    ProductFeatureSectionViewSet,
)

router = DefaultRouter()

router.register(r'banners',     MainBannerViewSet,            basename='banner')
router.register(r'events',      EventViewSet,                 basename='event')
router.register(r'gallery',     GalleryImageViewSet,          basename='gallery')
router.register(r'categories',  ProductCategoryViewSet,       basename='category')
router.register(r'motorcycles', MotorcycleProductViewSet,     basename='motorcycle')
router.register(r'colors',      ProductColorViewSet,          basename='color')
router.register(r'top-about',   ProductTopAboutViewSet,       basename='top-about')
router.register(r'features',    ProductFeatureSectionViewSet, basename='feature')

urlpatterns = router.urls