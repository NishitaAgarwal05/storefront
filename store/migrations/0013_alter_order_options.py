# Generated by Django 4.2.9 on 2024-01-27 11:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0012_alter_customer_options_remove_customer_email_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'permissions': [('cancel_order', 'Can cancel an order')]},
        ),
    ]
