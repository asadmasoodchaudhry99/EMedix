# Generated by Django 3.1.4 on 2021-08-01 13:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('video_app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='room',
            old_name='room_token',
            new_name='room_sid',
        ),
        migrations.RemoveField(
            model_name='person',
            name='gender',
        ),
        migrations.RemoveField(
            model_name='person',
            name='role',
        ),
        migrations.RemoveField(
            model_name='person',
            name='room',
        ),
    ]
