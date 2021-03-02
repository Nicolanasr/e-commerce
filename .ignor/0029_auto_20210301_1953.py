# Generated by Django 3.1.7 on 2021-03-01 17:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0028_rating'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='rating',
        ),
        migrations.AddField(
            model_name='rating',
            name='product_rated',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.product'),
        ),
    ]