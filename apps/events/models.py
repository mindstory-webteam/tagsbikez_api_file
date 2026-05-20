"""
apps/events/models.py

Model:
  Event  — upcoming ride / community event

Fields map directly to the JS data:
  title          → title
  startingPoint  → starting_point
  destination    → destination
  startdate      → start_date
  enddate        → end_date
  image          → image
  infoUrl        → info_url
"""

from django.db import models
from django.utils import timezone


class Event(models.Model):
    title          = models.CharField(max_length=300)
    starting_point = models.CharField(max_length=150, help_text='e.g. Thrissur')
    destination    = models.CharField(max_length=150, help_text='e.g. Kochi')
    start_date     = models.DateField()
    end_date       = models.DateField()
    image          = models.ImageField(upload_to='events/images/')
    info_url       = models.CharField(max_length=500, default='#', help_text='Link for "More Info" button')
    display_order  = models.PositiveIntegerField(default=0)
    is_active      = models.BooleanField(default=True)
    created_at     = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['start_date', 'display_order']
        verbose_name = 'Event'
        verbose_name_plural = 'Events'

    def __str__(self):
        return f"{self.title} ({self.start_date} → {self.end_date})"

    @property
    def is_upcoming(self):
        return self.end_date >= timezone.now().date()
