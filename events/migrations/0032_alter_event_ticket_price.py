# Generated by Django 3.2.7 on 2021-09-09 21:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0031_auto_20210909_2233'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='ticket_price',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
