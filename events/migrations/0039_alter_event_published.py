# Generated by Django 3.2.7 on 2021-09-10 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0038_auto_20210910_1304'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='published',
            field=models.BooleanField(default=True),
        ),
    ]