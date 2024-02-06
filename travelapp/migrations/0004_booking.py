# Generated by Django 5.0.1 on 2024-02-06 10:42

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travelapp', '0003_activity'),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('booking_type', models.CharField(choices=[('flight', 'Flight'), ('hotel', 'Hotel'), ('activity', 'Activity'), ('transfer', 'Transfer')], max_length=50)),
                ('booking_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('details', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('is_confirmed', models.BooleanField(default=False)),
                ('user_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to='travelapp.userprofile')),
            ],
        ),
    ]
