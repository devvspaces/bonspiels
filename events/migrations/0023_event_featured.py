# Generated by Django 3.2.5 on 2021-08-06 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0022_category_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='featured',
            field=models.BooleanField(default=False),
        ),
    ]
