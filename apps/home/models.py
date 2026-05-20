"""
apps/home/models.py

Models:
  MainBanner  — hero banner slides (image, title, subtitle, cta)
                supports 3 or more slides ordered by display_order
"""

from django.db import models


class MainBanner(models.Model):
    image         = models.ImageField(upload_to='home/banners/')
    title         = models.CharField(max_length=200, blank=True)
    subtitle      = models.CharField(max_length=300, blank=True)
    cta_label     = models.CharField(max_length=80,  blank=True, help_text='Button label e.g. "Explore Now"')
    cta_url       = models.CharField(max_length=300, blank=True, help_text='Button link URL or slug')
    display_order = models.PositiveIntegerField(default=0)
    is_active     = models.BooleanField(default=True)

    class Meta:
        ordering = ['display_order']
        verbose_name = 'Main Banner Slide'
        verbose_name_plural = 'Main Banner Slides'

    def __str__(self):
        return f"Banner #{self.display_order} — {self.title or 'Untitled'}"
