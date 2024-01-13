# Generated by Django 2.2 on 2023-12-08 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rail', '0006_user_info_last_login'),
    ]

    operations = [
        migrations.CreateModel(
            name='history',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=100)),
                ('train_no', models.IntegerField()),
                ('from_st', models.CharField(max_length=100)),
                ('to_st', models.CharField(max_length=100)),
                ('coach', models.CharField(max_length=100)),
                ('no_tickets', models.IntegerField()),
            ],
        ),
    ]
