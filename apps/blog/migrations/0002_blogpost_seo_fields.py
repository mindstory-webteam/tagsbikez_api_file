# Adds SEO fields (meta title, meta description, canonical URL) to BlogPost.

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='meta_title',
            field=models.CharField(
                blank=True,
                help_text='SEO <title> tag (max ~60-70 chars). Falls back to the post title if left blank.',
                max_length=70,
            ),
        ),
        migrations.AddField(
            model_name='blogpost',
            name='meta_description',
            field=models.CharField(
                blank=True,
                help_text='SEO meta description (max ~160 chars). Falls back to the excerpt if left blank.',
                max_length=160,
            ),
        ),
        migrations.AddField(
            model_name='blogpost',
            name='canonical_url',
            field=models.URLField(
                blank=True,
                help_text='Canonical URL for this post, e.g. "https://example.com/blog/my-post/". Leave blank to use the default post URL.',
                max_length=500,
            ),
        ),
    ]
