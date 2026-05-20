"""
apps/motorcycles/migrations/0001_initial.py
"""

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('categories', '0001_initial'),
    ]

    operations = [
        # ── MotorcycleProduct ─────────────────────────────────────────────
        migrations.CreateModel(
            name='MotorcycleProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True,
                                           serialize=False, verbose_name='ID')),
                ('name',              models.CharField(max_length=200)),
                ('slug',              models.SlugField(blank=True, max_length=220, unique=True)),
                ('featured_image',    models.ImageField(upload_to='motorcycles/images/')),
                ('short_description', models.CharField(max_length=500)),
                ('description',       models.TextField()),
                ('engine_cc',         models.CharField(max_length=50)),
                ('power',             models.CharField(max_length=50)),
                ('torque',            models.CharField(max_length=50)),
                ('brochure_file',     models.FileField(blank=True, null=True,
                                                       upload_to='motorcycles/brochures/')),
                ('display_order',     models.PositiveIntegerField(default=0)),
                ('is_active',         models.BooleanField(default=True)),
                ('created_at',        models.DateTimeField(auto_now_add=True)),
                ('updated_at',        models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='motorcycles',
                    to='categories.productcategory',
                )),
            ],
            options={
                'verbose_name': 'Motorcycle Product',
                'verbose_name_plural': 'Motorcycle Products',
                'ordering': ['display_order', 'name'],
            },
        ),

        # ── ProductColor ──────────────────────────────────────────────────
        migrations.CreateModel(
            name='ProductColor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True,
                                           serialize=False, verbose_name='ID')),
                ('name',          models.CharField(max_length=100)),
                ('hex',           models.CharField(max_length=10)),
                ('image',         models.ImageField(upload_to='motorcycles/colors/')),
                ('price',         models.CharField(max_length=30)),
                ('display_order', models.PositiveIntegerField(default=0)),
                ('motorcycle', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='colors',
                    to='motorcycles.motorcycleproduct',
                )),
            ],
            options={
                'verbose_name': 'Product Color',
                'verbose_name_plural': 'Product Colors',
                'ordering': ['display_order'],
            },
        ),

        # ── ProductTopAbout ───────────────────────────────────────────────
        migrations.CreateModel(
            name='ProductTopAbout',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True,
                                           serialize=False, verbose_name='ID')),
                ('top_image',   models.ImageField(upload_to='motorcycles/top_about/')),
                ('heading',     models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('motorcycle', models.OneToOneField(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='top_about',
                    to='motorcycles.motorcycleproduct',
                )),
            ],
            options={
                'verbose_name': 'Product Top About Section',
                'verbose_name_plural': 'Product Top About Sections',
            },
        ),

        # ── ProductFeatureSection ─────────────────────────────────────────
        migrations.CreateModel(
            name='ProductFeatureSection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True,
                                           serialize=False, verbose_name='ID')),
                ('image',         models.ImageField(upload_to='motorcycles/features/')),
                ('title',         models.CharField(max_length=200)),
                ('description',   models.TextField()),
                ('display_order', models.PositiveIntegerField(default=0)),
                ('motorcycle', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='features',
                    to='motorcycles.motorcycleproduct',
                )),
            ],
            options={
                'verbose_name': 'Product Feature Section',
                'verbose_name_plural': 'Product Feature Sections',
                'ordering': ['display_order'],
            },
        ),
    ]
