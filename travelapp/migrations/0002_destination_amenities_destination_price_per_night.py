# Generated by Django 5.0.1 on 2024-03-21 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travelapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='destination',
            name='amenities',
            field=models.JSONField(default=list),
        ),
        migrations.AddField(
            model_name='destination',
            name='price_per_night',
            field=models.DecimalField(decimal_places=2, default=500.0, max_digits=6),
            preserve_default=False,
        ),
    ]
