# Generated by Django 4.2 on 2023-07-03 04:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_product_desc'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='model_number',
        ),
        migrations.RemoveField(
            model_name='product',
            name='mop',
        ),
        migrations.AlterField(
            model_name='product',
            name='mrp',
            field=models.DecimalField(decimal_places=1, max_digits=8),
        ),
    ]