# Generated by Django 5.1.3 on 2024-11-21 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatBot', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='threadswithtimestamps',
            name='timestamp',
            field=models.DateTimeField(max_length=100),
        ),
    ]