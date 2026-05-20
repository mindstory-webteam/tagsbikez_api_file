import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True
    dependencies = []

    operations = [
        migrations.CreateModel(
            name='GalleryAlbum',
            fields=[
                ('id',            models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title',         models.CharField(max_length=200)),
                ('slug',          models.SlugField(blank=True, max_length=220, unique=True)),
                ('cover_image',   models.ImageField(upload_to='gallery/covers/')),
                ('description',   models.TextField(blank=True)),
                ('display_order', models.PositiveIntegerField(default=0)),
                ('is_active',     models.BooleanField(default=True)),
                ('created_at',    models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Gallery Album',
                'verbose_name_plural': 'Gallery Albums',
                'ordering': ['display_order', '-created_at'],
            },
        ),
        migrations.CreateModel(
            name='GalleryImage',
            fields=[
                ('id',            models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image',         models.ImageField(upload_to='gallery/images/')),
                ('caption',       models.CharField(blank=True, max_length=300)),
                ('display_order', models.PositiveIntegerField(default=0)),
                ('is_active',     models.BooleanField(default=True)),
                ('uploaded_at',   models.DateTimeField(auto_now_add=True)),
                ('album', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='images',
                    to='gallery.galleryalbum',
                )),
            ],
            options={
                'verbose_name': 'Gallery Image',
                'verbose_name_plural': 'Gallery Images',
                'ordering': ['display_order', 'uploaded_at'],
            },
        ),
    ]
