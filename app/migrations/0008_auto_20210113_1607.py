# Generated by Django 3.1.5 on 2021-01-13 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_auto_20210113_1054'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rate',
            name='score',
            field=models.FloatField(blank=True, default=1),
        ),
    ]
