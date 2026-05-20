from django.db import models
from django.utils.text import slugify


class ProductCategory(models.Model):
    name          = models.CharField(max_length=100, unique=True)
    slug          = models.SlugField(max_length=120, unique=True, blank=True)
    is_active     = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['display_order', 'name']
        verbose_name = 'Product Category'
        verbose_name_plural = 'Product Categories'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name