# Generated by Django 3.2.7 on 2021-09-09 21:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0029_event_published'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='eventspeaker',
            name='event',
        ),
        migrations.RemoveField(
            model_name='ticket',
            name='event',
        ),
        migrations.RemoveField(
            model_name='ticket',
            name='featuring',
        ),
        migrations.AlterModelOptions(
            name='event',
            options={'ordering': ['start_date']},
        ),
        migrations.RenameField(
            model_name='event',
            old_name='e_time',
            new_name='end_date',
        ),
        migrations.RenameField(
            model_name='event',
            old_name='s_time',
            new_name='start_date',
        ),
        migrations.RemoveField(
            model_name='event',
            name='city',
        ),
        migrations.RemoveField(
            model_name='userticket',
            name='ticket',
        ),
        migrations.AddField(
            model_name='event',
            name='ticket_currency',
            field=models.CharField(choices=[('NGN', 'Nigerian naira'), ('USD', 'United States Dollar'), ('GBR', 'British Pounds'), ('EUR', 'Euro')], default=1, max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='event',
            name='ticket_name',
            field=models.CharField(default=1, max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='event',
            name='ticket_price',
            field=models.FloatField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userticket',
            name='event',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='events.event'),
            preserve_default=False,
        ),
        migrations.RemoveField(
            model_name='event',
            name='category',
        ),
        migrations.AddField(
            model_name='event',
            name='category',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='events.category'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='EventSchedule',
        ),
        migrations.DeleteModel(
            name='EventSpeaker',
        ),
        migrations.DeleteModel(
            name='Feature',
        ),
        migrations.DeleteModel(
            name='Ticket',
        ),
    ]
