# Generated by Django 5.0.2 on 2024-03-30 22:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0003_serviceorder_updated_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='serviceorder',
            name='updated_at',
        ),
        migrations.AddField(
            model_name='serviceorder',
            name='concluded_at',
            field=models.DateTimeField(null=True),
        ),
    ]