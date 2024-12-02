# Generated by Django 5.0.6 on 2024-12-02 17:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_remove_product_last_updated_product_created_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='is_published',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='product',
            name='product_uom',
            field=models.CharField(default='stuk', max_length=100),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='ProductPriceLine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='price_lines', to='product.product')),
            ],
        ),
    ]