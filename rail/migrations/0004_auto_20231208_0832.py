# Generated by Django 2.2 on 2023-12-08 03:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rail', '0003_user_info_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_info',
            name='is_verified',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='user_info',
            name='otp',
            field=models.IntegerField(default=0),
        ),
    ]
