from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True
    dependencies = []

    operations = [
        migrations.CreateModel(
            name='MainBanner',
            fields=[
                ('id',            models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image',         models.ImageField(upload_to='home/banners/')),
                ('title',         models.CharField(blank=True, max_length=200)),
                ('subtitle',      models.CharField(blank=True, max_length=300)),
                ('cta_label',     models.CharField(blank=True, max_length=80)),
                ('cta_url',       models.CharField(blank=True, max_length=300)),
                ('display_order', models.PositiveIntegerField(default=0)),
                ('is_active',     models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Main Banner Slide',
                'verbose_name_plural': 'Main Banner Slides',
                'ordering': ['display_order'],
            },
        ),
    ]
