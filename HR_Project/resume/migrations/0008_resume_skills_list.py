# Generated by Django 4.2.7 on 2023-12-08 21:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resume', '0007_resume_phone_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='resume',
            name='skills_list',
            field=models.TextField(blank=True, max_length=500, null=True),
        ),
    ]
