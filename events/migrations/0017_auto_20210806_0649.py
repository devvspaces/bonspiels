# Generated by Django 3.2.5 on 2021-08-06 05:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0016_eventcalendar_eventlike_eventreview_eventview_reviewimage'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventreview',
            name='comment',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='eventreview',
            name='stars',
            field=models.IntegerField(default=0),
        ),
    ]
