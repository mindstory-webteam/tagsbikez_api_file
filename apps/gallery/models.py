from django.db import models


class GalleryImage(models.Model):
    image         = models.ImageField(upload_to='gallery/images/')
    caption       = models.CharField(max_length=300, blank=True)
    display_order = models.PositiveIntegerField(default=0)
    is_active     = models.BooleanField(default=True)
    uploaded_at   = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['display_order', 'uploaded_at']
        verbose_name = 'Gallery Image'
        verbose_name_plural = 'Gallery Images'

    def __str__(self):
        return f"Image #{self.display_order} — {self.caption or 'No caption'}"