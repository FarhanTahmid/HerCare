# Generated by Django 5.1.3 on 2024-11-21 05:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ThreadsWithTimeStamps',
            fields=[
                ('thread_id', models.CharField(max_length=200, primary_key=True, serialize=False)),
                ('timestamp', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'Conversation Threads and Timestamps',
            },
        ),
    ]
