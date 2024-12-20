# Generated by Django 5.0.6 on 2024-11-28 18:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='original_price',
            new_name='price',
        ),
        migrations.RemoveField(
            model_name='product',
            name='discount_amount',
        ),
        migrations.RemoveField(
            model_name='product',
            name='discount_price',
        ),
        migrations.RemoveField(
            model_name='product',
            name='is_discounted',
        ),
        migrations.RemoveField(
            model_name='product',
            name='product_category',
        ),
    ]
