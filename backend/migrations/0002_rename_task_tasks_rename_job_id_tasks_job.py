# Generated by Django 5.0.6 on 2024-06-09 09:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Task',
            new_name='Tasks',
        ),
        migrations.RenameField(
            model_name='tasks',
            old_name='job_id',
            new_name='job',
        ),
    ]
