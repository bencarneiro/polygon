# Generated by Django 3.2 on 2023-02-26 23:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nft', '0003_auto_20230226_2358'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seaporttransaction',
            name='gas_price',
            field=models.BigIntegerField(default=0),
        ),
    ]
