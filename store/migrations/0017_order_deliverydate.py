# Generated by Django 3.1.7 on 2021-02-23 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0016_order_shipped'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='deliveryDate',
            field=models.DateField(blank=True, null=True),
        ),
    ]
