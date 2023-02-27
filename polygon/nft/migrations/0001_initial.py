# Generated by Django 3.2 on 2023-02-26 22:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SeaportTransaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tx_hash', models.CharField(max_length=100)),
                ('method_name', models.CharField(max_length=100)),
                ('value', models.IntegerField(default=0)),
                ('gas_price', models.IntegerField(default=0)),
                ('gas_used', models.IntegerField(default=0)),
                ('tx_fee', models.IntegerField(default=0)),
                ('tx_reciept_status', models.BooleanField(default=0)),
                ('dt', models.DateTimeField()),
                ('block_number', models.PositiveIntegerField()),
                ('is_error', models.BooleanField(default=0)),
                ('to_address', models.CharField(max_length=100)),
                ('from_address', models.CharField(max_length=100)),
                ('token_contract_address', models.CharField(blank=True, max_length=100, null=True)),
                ('token_id', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'db_table': 'seaport_transaction',
                'managed': True,
            },
        ),
    ]