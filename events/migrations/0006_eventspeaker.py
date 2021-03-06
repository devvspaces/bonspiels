# Generated by Django 3.2.5 on 2021-07-31 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0005_alter_event_amenities'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventSpeaker',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('image', models.ImageField(upload_to='events/speakers')),
                ('designation', models.CharField(max_length=30)),
            ],
        ),
    ]
