# Generated by Django 3.1.7 on 2021-03-02 07:11

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0030_product_avg_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='avg_rating',
            field=models.FloatField(blank=True, default=0, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)]),
        ),
    ]