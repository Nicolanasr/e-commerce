# Generated by Django 3.1.7 on 2021-03-02 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0034_product_avg_ratings'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='avg_ratings',
            field=models.FloatField(blank=True, default=models.FloatField(blank=True, null=True), null=True),
        ),
    ]