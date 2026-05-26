"""
apps/api/urls.py

Central URL conf for the TagsBikez REST API.
Include in project urls.py:
    path('api/', include('apps.api.urls')),
"""

from django.urls import path
from .views import (
    MainBannerListView,
    EventListView,
    UpcomingEventListView,
    GalleryImageListView,
    ProductCategoryListView,
    ProductCategoryDetailView,
    MotorcycleProductListView,
    MotorcycleProductDetailView,
)

app_name = 'api'

urlpatterns = [
    # ── Banners ──────────────────────────────────────────────────────────────
    path('banners/',                    MainBannerListView.as_view(),          name='banner-list'),

    # ── Events ───────────────────────────────────────────────────────────────
    path('events/',                     EventListView.as_view(),               name='event-list'),
    path('events/upcoming/',            UpcomingEventListView.as_view(),       name='event-upcoming'),

    # ── Gallery ──────────────────────────────────────────────────────────────
    path('gallery/',                    GalleryImageListView.as_view(),        name='gallery-list'),

    # ── Categories ───────────────────────────────────────────────────────────
    path('categories/',                 ProductCategoryListView.as_view(),     name='category-list'),
    path('categories/<slug:slug>/',     ProductCategoryDetailView.as_view(),   name='category-detail'),

    # ── Motorcycles (colors nested inside — no /colors/ route) ───────────────
    path('motorcycles/',                MotorcycleProductListView.as_view(),   name='motorcycle-list'),
    path('motorcycles/<slug:slug>/',    MotorcycleProductDetailView.as_view(), name='motorcycle-detail'),
]