# Generated by Django 3.2.9 on 2022-01-05 12:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('download', '0002_full_tasks_id_full_tasks_list_tasks_celery_tasks_list'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='posts',
            name='task_id',
        ),
    ]
