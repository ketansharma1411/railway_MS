# Generated by Django 2.2 on 2023-12-07 19:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rail', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='train',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('train_name', models.CharField(max_length=100)),
                ('train_no', models.IntegerField()),
                ('no_tickets', models.IntegerField()),
            ],
        ),
    ]