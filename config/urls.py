"""
config/urls.py  — root URL configuration for TagsBikez
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # Django admin
    path('admin/', admin.site.urls),

    # REST API  — all endpoints live under /api/
    path('api/', include('apps.api.urls')),

    # DRF browsable API login (dev only)
    path('api-auth/', include('rest_framework.urls')),
]

# ── Serve uploaded media files in development ────────────────────────────────
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
