from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True
    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id',             models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title',          models.CharField(max_length=300)),
                ('starting_point', models.CharField(max_length=150)),
                ('destination',    models.CharField(max_length=150)),
                ('start_date',     models.DateField()),
                ('end_date',       models.DateField()),
                ('image',          models.ImageField(upload_to='events/images/')),
                ('info_url',       models.CharField(default='#', max_length=500)),
                ('display_order',  models.PositiveIntegerField(default=0)),
                ('is_active',      models.BooleanField(default=True)),
                ('created_at',     models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Event',
                'verbose_name_plural': 'Events',
                'ordering': ['start_date', 'display_order'],
            },
        ),
    ]
