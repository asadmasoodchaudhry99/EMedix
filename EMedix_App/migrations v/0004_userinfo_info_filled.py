# Generated by Django 3.1.4 on 2021-08-31 19:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EMedix_App', '0003_clinic_doctors'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='info_filled',
            field=models.BooleanField(default=False),
        ),
    ]
