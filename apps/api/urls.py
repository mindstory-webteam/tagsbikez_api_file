"""
apps/api/urls.py
Central URL conf for the TagsBikez REST API.
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
    CareerDepartmentListView,
    BlogPostListView,
    PopularBlogPostListView,
    BlogPostDetailView,
)

app_name = 'api'

urlpatterns = [
    # Banners
    path('banners/',                    MainBannerListView.as_view(),          name='banner-list'),
    # Events
    path('events/',                     EventListView.as_view(),               name='event-list'),
    path('events/upcoming/',            UpcomingEventListView.as_view(),       name='event-upcoming'),
    # Gallery
    path('gallery/',                    GalleryImageListView.as_view(),        name='gallery-list'),
    # Categories
    path('categories/',                 ProductCategoryListView.as_view(),     name='category-list'),
    path('categories/<slug:slug>/',     ProductCategoryDetailView.as_view(),   name='category-detail'),
    # Motorcycles
    path('motorcycles/',                MotorcycleProductListView.as_view(),   name='motorcycle-list'),
    path('motorcycles/<slug:slug>/',    MotorcycleProductDetailView.as_view(), name='motorcycle-detail'),
    # Careers
    path('careers/',                    CareerDepartmentListView.as_view(),    name='career-list'),
    # Blog  (keep 'popular/' BEFORE '<slug>/' so it isn't captured as a slug)
    path('blog/',                       BlogPostListView.as_view(),            name='blog-list'),
    path('blog/popular/',               PopularBlogPostListView.as_view(),    name='blog-popular'),
    path('blog/<slug:slug>/',           BlogPostDetailView.as_view(),         name='blog-detail'),
]