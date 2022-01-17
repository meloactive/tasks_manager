# Generated by Django 3.2.9 on 2021-11-02 07:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('download', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tasks_Celery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_id', models.CharField(max_length=40)),
                ('description', models.CharField(max_length=40)),
                ('progress', models.CharField(max_length=40)),
                ('status', models.CharField(max_length=40)),
                ('finished', models.CharField(max_length=40)),
            ],
        ),

        migrations.CreateModel(
            name='Tasks_List',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_id', models.CharField(max_length=40)),
                ('description', models.CharField(max_length=40)),
                ('extra_values', models.CharField(max_length=40)),
            ],
        ),

        migrations.CreateModel(
            name='Full_Tasks_List',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_id', models.CharField(max_length=40)),
                ('full_task_id', models.CharField(max_length=40)),
                ('user_inputs', models.CharField(max_length=40)),
                ('status', models.CharField(max_length=40)),
            ],
        ),

        migrations.CreateModel(
            name='Full_Tasks_ID',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_id', models.CharField(max_length=40)),
                ('status', models.CharField(max_length=40)),
            ],
        ),
    ]
