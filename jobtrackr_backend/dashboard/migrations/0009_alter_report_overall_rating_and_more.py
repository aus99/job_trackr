# Generated by Django 4.2.7 on 2024-02-06 23:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0008_alter_report_rating_distribution_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='overall_rating',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='report',
            name='rating_distribution',
            field=models.JSONField(default=dict),
        ),
        migrations.AlterField(
            model_name='report',
            name='top_reviews',
            field=models.JSONField(default=list),
        ),
    ]
