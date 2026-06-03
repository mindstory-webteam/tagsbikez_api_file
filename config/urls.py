"""
config/urls.py  — root URL configuration for TagsBikez
"""
# from django.contrib import admin
# from django.urls import path, include
# from django.conf import settings
# from django.conf.urls.static import static

# from rest_framework.decorators import api_view
# from rest_framework.response import Response


# @api_view(['GET'])
# def api_root(request):
#     return Response({
#         'banners':     request.build_absolute_uri('/api/banners/'),
#         'events':      request.build_absolute_uri('/api/events/'),
#         'upcoming':    request.build_absolute_uri('/api/events/upcoming/'),
#         'gallery':     request.build_absolute_uri('/api/gallery/'),
#         'categories':  request.build_absolute_uri('/api/categories/'),
#         'motorcycles': request.build_absolute_uri('/api/motorcycles/'),
#         'career': request.build_absolute_uri('/api/careers/'),
#     })


# urlpatterns = [
#     # Django admin
#     path('admin/', admin.site.urls),

#     # API root — shows all available endpoints
#     path('api/', api_root, name='api-root'),

#     # REST API — all endpoints live under /api/
#     path('api/', include('apps.api.urls')),

#     # DRF browsable API login (dev only)
#     path('api-auth/', include('rest_framework.urls')),
# ]

# # ── Serve uploaded media files in development ─────────────────────────────────
# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

    
"""
config/urls.py  — root URL configuration for TagsBikez
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def api_root(request):
    return Response({
        'banners':     request.build_absolute_uri('/api/banners/'),
        'events':      request.build_absolute_uri('/api/events/'),
        'upcoming':    request.build_absolute_uri('/api/events/upcoming/'),
        'gallery':     request.build_absolute_uri('/api/gallery/'),
        'categories':  request.build_absolute_uri('/api/categories/'),
        'motorcycles': request.build_absolute_uri('/api/motorcycles/'),
        'career': request.build_absolute_uri('/api/careers/'),
    })


urlpatterns = [
    # Django admin
    path('admin/', admin.site.urls),

    # API root — shows all available endpoints
    path('api/', api_root, name='api-root'),

    # REST API — all endpoints live under /api/
    path('api/', include('apps.api.urls')),

    # DRF browsable API login (dev only)
    path('api-auth/', include('rest_framework.urls')),

    # Motorcycles admin utilities (bulk import, etc.)
    path('admin/motorcycles/', include('apps.motorcycles.urls')),
]

# ── Serve uploaded media files in development ─────────────────────────────────
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)