# Generated by Django 5.0.2 on 2024-12-20 07:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0009_rename_product_name_product_name_product_ean'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='description',
            field=models.CharField(blank=True, max_length=2000, null=True),
        ),
    ]
