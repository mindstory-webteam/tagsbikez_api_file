from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='ProductCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('slug', models.SlugField(blank=True, max_length=120, unique=True)),
                ('category_image', models.ImageField(upload_to='categories/images/')),
                ('is_active', models.BooleanField(default=True)),
                ('display_order', models.PositiveIntegerField(default=0)),
            ],
            options={
                'verbose_name': 'Product Category',
                'verbose_name_plural': 'Product Categories',
                'ordering': ['display_order', 'name'],
            },
        ),
        migrations.CreateModel(
            name='ProductCategoryAbout',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('about_image', models.ImageField(upload_to='categories/about/')),
                ('about_name', models.CharField(max_length=200)),
                ('about_description', models.TextField()),
                ('category', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='about', to='categories.productcategory')),
            ],
            options={
                'verbose_name': 'Category About Section',
                'verbose_name_plural': 'Category About Sections',
            },
        ),
        migrations.CreateModel(
            name='ProductCategoryBottomSection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('about_image', models.ImageField(upload_to='categories/bottom/')),
                ('about_header', models.CharField(max_length=200)),
                ('about_description', models.TextField()),
                ('display_order', models.PositiveIntegerField(default=0)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bottom_sections', to='categories.productcategory')),
            ],
            options={
                'verbose_name': 'Category Bottom Section',
                'verbose_name_plural': 'Category Bottom Sections',
                'ordering': ['display_order'],
            },
        ),
    ]
