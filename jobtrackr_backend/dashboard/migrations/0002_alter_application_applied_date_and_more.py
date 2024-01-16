# Generated by Django 4.2.7 on 2023-11-29 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='applied_date',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='application',
            name='status',
            field=models.CharField(choices=[('applied', 'Applied'), ('screening', 'Screening'), ('interview', 'Interview'), ('offer', 'Offer'), ('rejected', 'Rejected')], max_length=10),
        ),
        migrations.AlterField(
            model_name='job',
            name='description',
            field=models.CharField(max_length=10000),
        ),
    ]
