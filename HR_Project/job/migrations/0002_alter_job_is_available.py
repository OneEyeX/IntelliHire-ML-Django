# Generated by Django 4.2.7 on 2023-11-26 03:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='is_available',
            field=models.BooleanField(default=True),
        ),
    ]