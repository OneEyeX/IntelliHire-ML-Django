# Generated by Django 4.2.7 on 2023-12-10 20:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0007_applyjob_matching_value'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applyjob',
            name='matching_value',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
    ]
