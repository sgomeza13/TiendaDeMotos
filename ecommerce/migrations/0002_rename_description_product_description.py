# Generated by Django 4.1 on 2023-09-08 13:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='Description',
            new_name='description',
        ),
    ]
