# Generated by Django 3.1.7 on 2021-02-26 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0019_order_coupon_activated'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='totalAfterCoupon',
            field=models.FloatField(blank=True, null=True),
        ),
    ]