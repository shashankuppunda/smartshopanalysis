# Generated by Django 4.2.2 on 2023-06-26 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_cart_prebook'),
    ]

    operations = [
        migrations.AddField(
            model_name='specialoffer',
            name='vendor_name',
            field=models.CharField(default=0, max_length=255),
            preserve_default=False,
        ),
    ]
