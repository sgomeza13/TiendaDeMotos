# Generated by Django 4.2.4 on 2023-09-12 03:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0006_orders_address_orders_city_orders_email_orders_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='address',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='orders',
            name='city',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='orders',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name='orders',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='orders',
            name='product',
            field=models.CharField(max_length=255),
        ),
    ]
