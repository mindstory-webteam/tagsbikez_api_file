"""
apps/blog/models.py

Mirrors the front-end `blogsData` shape exactly:

  {
    slug, title, excerpt,
    content: [ "para 1", "para 2", ... ],   <- plain-text paragraphs (NO html)
    author, date, popular, image
  }

Models
  BlogPost       - one article (title / slug / excerpt / author / date / popular / image)
  BlogParagraph  - one paragraph of the article body (ordered). Serialized into
                   the flat `content` array.
"""

from django.db import models
from django.utils.text import slugify
from django.utils import timezone


class BlogPost(models.Model):
    title   = models.CharField(max_length=300)
    slug    = models.SlugField(
        max_length=320,
        unique=True,
        blank=True,
        help_text='Auto-generated from the title if left blank. Used in the URL.',
    )
    excerpt = models.CharField(
        max_length=400,
        help_text='Short preview line shown on the card / sidebar.',
    )
    author  = models.CharField(
        max_length=120,
        default='Admin',
        help_text='By-line, e.g. "Admin".',
    )
    image   = models.ImageField(
        upload_to='blog/images/',
        help_text='Post image - used on the card, POPULAR sidebar and the detail page.',
    )

    popular        = models.BooleanField(
        default=False,
        help_text='ON -> this post appears in the POPULAR sidebar.',
    )
    published_date = models.DateField(
        default=timezone.now,
        help_text='Shown as "Mar 20, 2026".',
    )
    display_order  = models.PositiveIntegerField(default=0)
    is_active      = models.BooleanField(default=True)
    created_at     = models.DateTimeField(auto_now_add=True)
    updated_at     = models.DateTimeField(auto_now=True)

    class Meta:
        ordering            = ['-published_date', 'display_order', '-id']
        verbose_name        = 'Blog Post'
        verbose_name_plural = 'Blog Posts'
        indexes = [
            models.Index(fields=['is_active', '-published_date']),
            models.Index(fields=['popular', 'is_active']),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title)[:300] or 'post'
            slug = base
            n    = 2
            qs   = BlogPost.objects.exclude(pk=self.pk)
            while qs.filter(slug=slug).exists():
                slug = f'{base}-{n}'
                n += 1
            self.slug = slug
        super().save(*args, **kwargs)

    # -- Helpers for the API --------------------------------------------------
    @property
    def content_list(self):
        """The paragraphs as a plain list of strings -> the `content` array."""
        return list(self.paragraphs.order_by('display_order', 'id')
                                    .values_list('text', flat=True))

    def _siblings(self):
        return BlogPost.objects.filter(is_active=True).order_by(
            '-published_date', 'display_order', '-id'
        )

    def get_previous_post(self):
        ids = list(self._siblings().values_list('pk', flat=True))
        if self.pk in ids:
            i = ids.index(self.pk)
            if i > 0:
                return BlogPost.objects.filter(pk=ids[i - 1]).first()
        return None

    def get_next_post(self):
        ids = list(self._siblings().values_list('pk', flat=True))
        if self.pk in ids:
            i = ids.index(self.pk)
            if i < len(ids) - 1:
                return BlogPost.objects.filter(pk=ids[i + 1]).first()
        return None


class BlogParagraph(models.Model):
    post          = models.ForeignKey(
        BlogPost,
        on_delete=models.CASCADE,
        related_name='paragraphs',
    )
    text          = models.TextField(help_text='One paragraph of the article (plain text).')
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering            = ['display_order', 'id']
        verbose_name        = 'Paragraph'
        verbose_name_plural = 'Content Paragraphs'

    def __str__(self):
        preview = (self.text or '')[:50]
        return f'{self.post.title} - para {self.display_order}: {preview}'
