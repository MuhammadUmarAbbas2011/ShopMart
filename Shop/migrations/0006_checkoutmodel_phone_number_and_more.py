# Generated by Django 4.1.7 on 2025-02-04 08:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Shop', '0005_checkoutmodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='checkoutmodel',
            name='phone_number',
            field=models.CharField(default=2, max_length=15),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='checkoutmodel',
            name='shipping_address',
            field=models.TextField(default=3),
            preserve_default=False,
        ),
    ]
