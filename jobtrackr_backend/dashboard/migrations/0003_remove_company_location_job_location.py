# Generated by Django 4.2.7 on 2023-12-28 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_alter_application_applied_date_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='company',
            name='location',
        ),
        migrations.AddField(
            model_name='job',
            name='location',
            field=models.CharField(default='London', max_length=100),
        ),
    ]
