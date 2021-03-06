# Generated by Django 3.2.5 on 2021-07-31 11:44

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Amenity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('category', models.CharField(choices=[('1', 'Concerts'), ('2', 'Food fest'), ('3', 'Auto show')], max_length=10)),
                ('city', models.CharField(max_length=200)),
                ('location', models.CharField(max_length=200)),
                ('website_url', models.URLField()),
                ('description', models.TextField()),
                ('phone', models.CharField(max_length=25)),
                ('email', models.EmailField(max_length=254)),
                ('facebook', models.URLField(blank=True)),
                ('twitter', models.URLField(blank=True)),
                ('instagram', models.URLField(blank=True)),
                ('linkedin', models.URLField(blank=True)),
                ('dribble', models.URLField(blank=True)),
                ('digg', models.URLField(blank=True)),
                ('youtube', models.URLField(blank=True)),
                ('google_plus', models.URLField(blank=True)),
                ('featured_image', models.ImageField(upload_to='events')),
                ('seats', models.IntegerField()),
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('amenities', models.ManyToManyField(to='events.Amenity')),
            ],
        ),
        migrations.CreateModel(
            name='Feature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('price', models.FloatField()),
                ('row', models.IntegerField()),
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.event')),
                ('featuring', models.ManyToManyField(to='events.Feature')),
            ],
        ),
        migrations.CreateModel(
            name='Gallery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('image', models.ImageField(upload_to='events/gallery')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.event')),
            ],
        ),
    ]
