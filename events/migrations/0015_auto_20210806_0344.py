# Generated by Django 3.2.5 on 2021-08-06 02:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0014_auto_20210805_1410'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'Categories'},
        ),
        migrations.AddField(
            model_name='event',
            name='e_time',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='s_time',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='category',
            field=models.ManyToManyField(to='events.Category'),
        ),
    ]