# Generated by Django 5.1 on 2024-11-08 09:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0002_order_original_paid_order_stripe_pid'),
        ('user_profiles', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='user_profile',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to='user_profiles.userprofile'),
        ),
    ]