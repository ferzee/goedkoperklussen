# Generated by Django 5.0.4 on 2024-11-29 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sitemap', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitemap',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
