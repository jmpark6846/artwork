# Generated by Django 3.2.8 on 2021-10-22 05:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artwork', '0004_alter_product_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artwork',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
