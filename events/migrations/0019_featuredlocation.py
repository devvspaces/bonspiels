# Generated by Django 3.2.5 on 2021-08-06 07:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0018_auto_20210806_0731'),
    ]

    operations = [
        migrations.CreateModel(
            name='FeaturedLocation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
    ]