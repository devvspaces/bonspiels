# Generated by Django 3.2.7 on 2021-09-10 20:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0041_auto_20210910_1343'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userticket',
            name='name',
        ),
        migrations.RemoveField(
            model_name='userticket',
            name='phone',
        ),
        migrations.AddField(
            model_name='userticket',
            name='information',
            field=models.CharField(blank=True, max_length=700),
        ),
        migrations.AlterField(
            model_name='event',
            name='inform_tools_conf',
            field=models.CharField(blank=True, editable=False, max_length=700),
        ),
    ]
