# Generated by Django 4.1.7 on 2024-01-17 06:27

import django.contrib.postgres.indexes
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("address", "0004_address_custom_migration"),
    ]

    operations = [
        migrations.AddIndex(
            model_name="address",
            index=django.contrib.postgres.indexes.GinIndex(
                fields=["combined_address"],
                name="address_add_combine_fa4d70_gin",
                opclasses=["gin_trgm_ops"],
            ),
        ),
    ]
