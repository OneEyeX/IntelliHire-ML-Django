# Generated by Django 4.2.7 on 2023-12-08 22:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('resume', '0009_rename_skills_list_resume_skills'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='resume',
            name='phone_number',
        ),
        migrations.RemoveField(
            model_name='resume',
            name='skills',
        ),
    ]