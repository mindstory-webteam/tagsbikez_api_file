"""
apps/motorcycles/urls.py
Admin-side URLs for the motorcycles app (bulk import, etc.)
"""
from django.urls import path
from .bulk_import import bulk_import_view

app_name = "motorcycles"

urlpatterns = [
    path("bulk-import/", bulk_import_view, name="bulk_import"),
]
