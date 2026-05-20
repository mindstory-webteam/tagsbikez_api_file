"""
apps/motorcycles/models.py

Models:
  MotorcycleProduct        — core product (name, slug, category, description,
                             featured_image, specs, brochure)
  ProductColor             — per-color variant with its own image + price
  ProductTopAbout          — top hero section (image + heading + description)
  ProductFeatureSection    — bottom story cards (image + title + description)

Page layout the models power
─────────────────────────────
  [ProductTopAbout]          ← TOP: Image / Heading / Description
  ──────────────────────────
  [MotorcycleProduct]        ← DETAIL PANEL
    • name / price (from selected ProductColor)
    • description
    • colors  (ProductColor queryset)
    • engine_cc / power / torque
    • brochure_file
  ──────────────────────────
  [ProductFeatureSection ×N] ← BOTTOM: Image / Title / Description
"""

from django.db import models
from django.utils.text import slugify


# ─────────────────────────────────────────────────────────────────────────────
# MOTORCYCLE PRODUCT
# ─────────────────────────────────────────────────────────────────────────────

class MotorcycleProduct(models.Model):
    category = models.ForeignKey(
        'categories.ProductCategory',
        on_delete=models.CASCADE,
        related_name='motorcycles',
    )
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)

    # Main product image (used in listings / hero)
    featured_image = models.ImageField(upload_to='motorcycles/images/')

    # Short blurb shown on listing cards
    short_description = models.CharField(max_length=500)

    # Full description shown in the detail panel
    description = models.TextField()

    # ── Specs ──────────────────────────────────────────────────────────────
    engine_cc = models.CharField(max_length=50, help_text='e.g. 349cc')
    power     = models.CharField(max_length=50, help_text='e.g. 20.2 bhp')
    torque    = models.CharField(max_length=50, help_text='e.g. 27 Nm')

    # ── Brochure ───────────────────────────────────────────────────────────
    brochure_file = models.FileField(
        upload_to='motorcycles/brochures/',
        blank=True,
        null=True,
        help_text='Upload PDF brochure'
    )

    # ── Meta ───────────────────────────────────────────────────────────────
    display_order = models.PositiveIntegerField(default=0)
    is_active     = models.BooleanField(default=True)
    created_at    = models.DateTimeField(auto_now_add=True)
    updated_at    = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['display_order', 'name']
        verbose_name = 'Motorcycle Product'
        verbose_name_plural = 'Motorcycle Products'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


# ─────────────────────────────────────────────────────────────────────────────
# COLOR VARIANT
# ─────────────────────────────────────────────────────────────────────────────

class ProductColor(models.Model):
    motorcycle = models.ForeignKey(
        MotorcycleProduct,
        on_delete=models.CASCADE,
        related_name='colors',
    )
    name  = models.CharField(max_length=100, help_text='e.g. Factory Black')
    hex   = models.CharField(max_length=10,  help_text='e.g. #111111')
    image = models.ImageField(upload_to='motorcycles/colors/')
    price = models.CharField(max_length=30,  help_text='e.g. ₹1,69,189')
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['display_order']
        verbose_name = 'Product Color'
        verbose_name_plural = 'Product Colors'

    def __str__(self):
        return f"{self.motorcycle.name} — {self.name} ({self.price})"


# ─────────────────────────────────────────────────────────────────────────────
# TOP ABOUT SECTION  (hero above the detail panel)
# ─────────────────────────────────────────────────────────────────────────────

class ProductTopAbout(models.Model):
    """
    One-to-one top hero section per motorcycle.

    Fields map directly to the spec:
      Image       → top_image
      Heading     → heading
      Description → description
    """
    motorcycle = models.OneToOneField(
        MotorcycleProduct,
        on_delete=models.CASCADE,
        related_name='top_about',
    )
    top_image   = models.ImageField(upload_to='motorcycles/top_about/')
    heading     = models.CharField(max_length=200)
    description = models.TextField()

    class Meta:
        verbose_name = 'Product Top About Section'
        verbose_name_plural = 'Product Top About Sections'

    def __str__(self):
        return f"Top About — {self.motorcycle.name}"


# ─────────────────────────────────────────────────────────────────────────────
# BOTTOM FEATURE / STORY SECTIONS
# ─────────────────────────────────────────────────────────────────────────────

class ProductFeatureSection(models.Model):
    """
    Multiple story cards shown below the detail panel.

    Fields map directly to the spec:
      Image       → image
      Title       → title
      Description → description
    """
    motorcycle = models.ForeignKey(
        MotorcycleProduct,
        on_delete=models.CASCADE,
        related_name='features',
    )
    image         = models.ImageField(upload_to='motorcycles/features/')
    title         = models.CharField(max_length=200)
    description   = models.TextField()
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['display_order']
        verbose_name = 'Product Feature Section'
        verbose_name_plural = 'Product Feature Sections'

    def __str__(self):
        return f"{self.motorcycle.name} — {self.title}"
