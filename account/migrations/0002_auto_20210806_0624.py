# Generated by Django 3.2.5 on 2021-08-06 05:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='first_name',
            field=models.CharField(default='Ayomide', max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='profile',
            name='last_name',
            field=models.CharField(default='Ayanwola', max_length=30),
            preserve_default=False,
        ),
    ]
