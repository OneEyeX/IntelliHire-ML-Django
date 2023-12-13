# Generated by Django 4.2.7 on 2023-12-09 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resume', '0010_remove_resume_phone_number_remove_resume_skills'),
    ]

    operations = [
        migrations.AddField(
            model_name='resume',
            name='phone_number',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='resume',
            name='skills',
            field=models.TextField(blank=True, max_length=500, null=True),
        ),
    ]
