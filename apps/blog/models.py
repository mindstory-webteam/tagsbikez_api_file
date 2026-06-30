"""
apps/blog/models.py

Model:
  BlogPost — a single blog article.

Field → design mapping
──────────────────────────────────────────────────────────────────────────────
  LISTING CARD (blogs.png)
    featured_image     → card thumbnail
    title              → card heading ("Hunter 350: The New Rebel on the Streets")
    excerpt            → 1–2 line preview under the title ("READ MORE")
    author             → "Admin"
    published_date     → "Mar 20, 2026"

  POPULAR SIDEBAR (blogs.png)
    is_popular = True  → post appears in the POPULAR list
    featured_image     → small square thumbnail
    title / author / published_date

  DETAIL / INNER PAGE (hunter-350-the-new-rebel.png)
    title              → hero title + breadcrumb
    author / published_date → "Admin - Mar 05, 2026"
    intro              → lead paragraph under the title
    highlight          → the big RED sub-heading
    body_image         → image beside the body text
    body_image_caption → "1/3 Scenic riding route captured"
    body               → the rich HTML body area  ← "inner page html body"
    meta_description   → <meta> tag for SEO
    previous / next    → derived automatically from ordering (see API serializer)
"""

from django.db import models
from django.utils.text import slugify
from django.utils import timezone


class BlogPost(models.Model):
    # ── Headline ───────────────────────────────────────────────────────────
    title = models.CharField(max_length=300)
    slug  = models.SlugField(
        max_length=320,
        unique=True,
        blank=True,
        help_text='Auto-generated from the title if left blank. Used in the URL.',
    )
    author = models.CharField(
        max_length=120,
        default='Admin',
        help_text='Shown as the by-line, e.g. "Admin".',
    )

    # ── Media ──────────────────────────────────────────────────────────────
    featured_image = models.ImageField(
        upload_to='blog/featured/',
        help_text='Main image — used on the listing card, the POPULAR sidebar '
                  'thumbnail and the detail page.',
    )
    body_image = models.ImageField(
        upload_to='blog/body/',
        blank=True, null=True,
        help_text='Optional secondary image shown next to the body text on the '
                  'detail page.',
    )
    body_image_caption = models.CharField(
        max_length=200,
        blank=True,
        help_text='Caption under the body image, e.g. "1/3 Scenic riding route captured".',
    )

    # ── Copy ───────────────────────────────────────────────────────────────
    excerpt = models.CharField(
        max_length=300,
        help_text='Short preview shown on the listing card / sidebar.',
    )
    intro = models.TextField(
        blank=True,
        help_text='Lead paragraph shown directly under the title on the detail page.',
    )
    highlight = models.CharField(
        max_length=300,
        blank=True,
        help_text='The large RED sub-heading on the detail page (optional).',
    )
    body = models.TextField(
        help_text='Main article content. HTML is allowed — this is rendered as raw '
                  'HTML on the inner page (use <p>, <h3>, <strong>, <ul>, etc.).',
    )

    # ── SEO ────────────────────────────────────────────────────────────────
    meta_description = models.CharField(
        max_length=300,
        blank=True,
        help_text='Optional description for the page <meta> tag / link previews.',
    )

    # ── Flags & ordering ───────────────────────────────────────────────────
    is_popular     = models.BooleanField(
        default=False,
        help_text='ON → this post is listed in the POPULAR sidebar.',
    )
    published_date = models.DateField(
        default=timezone.now,
        help_text='Date shown on cards and the detail page.',
    )
    display_order  = models.PositiveIntegerField(default=0)
    is_active      = models.BooleanField(default=True)
    created_at     = models.DateTimeField(auto_now_add=True)
    updated_at     = models.DateTimeField(auto_now=True)

    class Meta:
        # Newest first; display_order lets editors pin/force a manual order.
        ordering            = ['-published_date', 'display_order', '-id']
        verbose_name        = 'Blog Post'
        verbose_name_plural = 'Blog Posts'
        indexes = [
            models.Index(fields=['is_active', '-published_date']),
            models.Index(fields=['is_popular', 'is_active']),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base   = slugify(self.title)[:300] or 'post'
            slug   = base
            n      = 2
            # Guarantee uniqueness without clashing with existing slugs.
            qs = BlogPost.objects.exclude(pk=self.pk)
            while qs.filter(slug=slug).exists():
                slug = f'{base}-{n}'
                n += 1
            self.slug = slug
        super().save(*args, **kwargs)

    # ── Helpers used by the API serializers ────────────────────────────────
    @property
    def read_time_minutes(self):
        """Rough reading time from the body word count (≈200 wpm, min 1)."""
        import re
        text  = re.sub(r'<[^>]+>', ' ', self.body or '')
        words = len(text.split())
        return max(1, round(words / 200))

    def _siblings(self):
        """Active posts in the same display order as the listing/detail pages."""
        return BlogPost.objects.filter(is_active=True).order_by(
            '-published_date', 'display_order', '-id'
        )

    def get_previous_post(self):
        """The newer neighbour (shown as PREVIOUS in the design)."""
        siblings = list(self._siblings().values_list('pk', flat=True))
        if self.pk in siblings:
            i = siblings.index(self.pk)
            if i > 0:
                return BlogPost.objects.filter(pk=siblings[i - 1]).first()
        return None

    def get_next_post(self):
        """The older neighbour (shown as NEXT in the design)."""
        siblings = list(self._siblings().values_list('pk', flat=True))
        if self.pk in siblings:
            i = siblings.index(self.pk)
            if i < len(siblings) - 1:
                return BlogPost.objects.filter(pk=siblings[i + 1]).first()
        return None
