# Generated by Django 3.2.5 on 2021-08-10 03:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0023_event_featured'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserTicket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=20)),
                ('attendees', models.IntegerField(default=1)),
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('ticket', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='events.ticket')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
