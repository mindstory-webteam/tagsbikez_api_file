"""
apps/motorcycles/models.py
"""

from django.db import models
from django.utils.text import slugify


class MotorcycleProduct(models.Model):
    category = models.ForeignKey(
        'categories.ProductCategory',
        on_delete=models.CASCADE,
        related_name='motorcycles',
    )
    name              = models.CharField(max_length=200)
    slug              = models.SlugField(max_length=220, unique=True, blank=True)
    featured_image    = models.ImageField(upload_to='motorcycles/images/')
    short_description = models.CharField(max_length=500)
    description       = models.TextField()

    # ── Specs ──────────────────────────────────────────────────────────────
    engine_cc = models.CharField(max_length=50, help_text='e.g. 349cc')
    power     = models.CharField(max_length=50, help_text='e.g. 20.2 bhp')
    torque    = models.CharField(max_length=50, help_text='e.g. 27 Nm')

    # ── Pricing ────────────────────────────────────────────────────────────
    emi_starts_at = models.CharField(
        max_length=100,
        blank=True,
        help_text='e.g. ₹3,999/month  — shown as "EMI STARTS @" on listing card',
    )

    # ── Brochure ───────────────────────────────────────────────────────────
    brochure_file = models.FileField(
        upload_to='motorcycles/brochures/',
        blank=True, null=True,
        help_text='Upload PDF brochure',
    )

    # ── Visibility ─────────────────────────────────────────────────────────
    coming_soon   = models.BooleanField(
        default=False,
        help_text=(
            'ON  → hides full detail page; shows "Coming Soon" badge on listing card.\n'
            'OFF → full detail page is accessible normally.'
        ),
    )
    display_order = models.PositiveIntegerField(default=0)
    is_active     = models.BooleanField(default=True)
    created_at    = models.DateTimeField(auto_now_add=True)
    updated_at    = models.DateTimeField(auto_now=True)

    class Meta:
        ordering            = ['display_order', 'name']
        verbose_name        = 'Motorcycle Product'
        verbose_name_plural = 'Motorcycle Products'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class ProductColor(models.Model):
    motorcycle    = models.ForeignKey(MotorcycleProduct, on_delete=models.CASCADE, related_name='colors')
    name          = models.CharField(max_length=100, help_text='e.g. Factory Black')
    hex           = models.CharField(max_length=10,  help_text='e.g. #111111')
    image         = models.ImageField(upload_to='motorcycles/colors/')
    price         = models.CharField(max_length=30,  help_text='e.g. ₹1,69,189')
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering            = ['display_order']
        verbose_name        = 'Product Color'
        verbose_name_plural = 'Product Colors'

    def __str__(self):
        return f"{self.motorcycle.name} — {self.name} ({self.price})"


class ProductTopAbout(models.Model):
    motorcycle  = models.OneToOneField(
        MotorcycleProduct, on_delete=models.CASCADE, related_name='top_about',
    )
    top_image   = models.ImageField(
        upload_to='motorcycles/top_about/',
        help_text='Hero image shown at the top of the product page',
    )
    heading     = models.CharField(max_length=200, help_text='e.g. Born to Ride')
    description = models.TextField(help_text='Paragraph shown below the heading')

    class Meta:
        verbose_name        = 'Product Top About Section'
        verbose_name_plural = 'Product Top About Sections'

    def __str__(self):
        return f"Top About — {self.motorcycle.name}"


class ProductFeatureSection(models.Model):
    motorcycle    = models.ForeignKey(
        MotorcycleProduct, on_delete=models.CASCADE, related_name='features',
    )
    image         = models.ImageField(
        upload_to='motorcycles/features/',
        help_text='Feature highlight image',
    )
    title         = models.CharField(max_length=200, help_text='e.g. Twin-pod Console')
    description   = models.TextField(help_text='Feature description paragraph')
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering            = ['display_order']
        verbose_name        = 'Product Feature Section'
        verbose_name_plural = 'Product Feature Sections (Bottom)'

    def __str__(self):
        return f"{self.motorcycle.name} — {self.title}"