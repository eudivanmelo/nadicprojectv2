# Generated by Django 5.0.2 on 2024-03-30 20:46

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0002_customer_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='serviceorder',
            name='updated_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]