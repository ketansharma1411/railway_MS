# Generated by Django 2.2 on 2023-12-08 02:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rail', '0002_train'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_info',
            name='email',
            field=models.CharField(default=0, max_length=100),
            preserve_default=False,
        ),
    ]
