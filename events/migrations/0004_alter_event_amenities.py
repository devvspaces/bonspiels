# Generated by Django 3.2.5 on 2021-07-31 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_rename_website_url_event_website'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='amenities',
            field=models.ManyToManyField(null=True, to='events.Amenity'),
        ),
    ]
