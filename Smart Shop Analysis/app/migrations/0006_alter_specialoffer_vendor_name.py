# Generated by Django 4.2.2 on 2023-06-26 10:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_specialoffer_vendor_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='specialoffer',
            name='vendor_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='uploaded_specialoffer', to=settings.AUTH_USER_MODEL),
        ),
    ]