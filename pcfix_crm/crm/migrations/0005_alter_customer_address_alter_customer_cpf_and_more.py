# Generated by Django 5.0.2 on 2024-03-31 15:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0004_remove_serviceorder_updated_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='address',
            field=models.CharField(help_text='Address of the customer.', max_length=200),
        ),
        migrations.AlterField(
            model_name='customer',
            name='cpf',
            field=models.CharField(help_text='CPF number of the customer.', max_length=11, unique=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, help_text='Date and time when the customer record was created.'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='email',
            field=models.EmailField(help_text='Email address of the customer.', max_length=254),
        ),
        migrations.AlterField(
            model_name='customer',
            name='first_name',
            field=models.CharField(help_text='First name of the customer.', max_length=50),
        ),
        migrations.AlterField(
            model_name='customer',
            name='last_name',
            field=models.CharField(help_text='Last name of the customer.', max_length=50),
        ),
        migrations.AlterField(
            model_name='customer',
            name='phone',
            field=models.CharField(help_text='Phone number of the customer.', max_length=20),
        ),
        migrations.AlterField(
            model_name='serviceorder',
            name='client',
            field=models.ForeignKey(help_text='The client associated with the service order.', on_delete=django.db.models.deletion.CASCADE, to='crm.customer'),
        ),
        migrations.AlterField(
            model_name='serviceorder',
            name='concluded_at',
            field=models.DateTimeField(help_text='Date and time when the service order was concluded (nullable).', null=True),
        ),
        migrations.AlterField(
            model_name='serviceorder',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, help_text='Date and time when the service order was created.'),
        ),
        migrations.AlterField(
            model_name='serviceorder',
            name='description',
            field=models.TextField(help_text='Description of the service order.'),
        ),
        migrations.AlterField(
            model_name='serviceorder',
            name='status',
            field=models.CharField(choices=[('budgeting', 'Budgeting'), ('approved_budget', 'Approved budget'), ('under_maintenance', 'Under maintenance'), ('concluded', 'Concluded'), ('delivered', 'Delivered')], help_text='Current status of the service order.', max_length=20),
        ),
        migrations.AlterField(
            model_name='serviceorder',
            name='value',
            field=models.DecimalField(blank=True, decimal_places=2, help_text='Value of the service order (nullable).', max_digits=8, null=True),
        ),
    ]
