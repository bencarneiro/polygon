from django.db import models

# Create your models here.

class SeaportTransaction(models.Model):

    tx_hash = models.CharField(primary_key=True, max_length=100, blank=False, null=False)
    method_name = models.CharField(max_length=256, blank=False, null=False)
    value = models.DecimalField( max_digits=65, decimal_places=0)
    gas_price = models.BigIntegerField(null=False, default=0)
    gas_used = models.BigIntegerField(null=False, default=0)
    tx_fee = models.BigIntegerField(null=False, default=0)
    tx_reciept_status = models.BooleanField(default=0)
    dt = models.DateTimeField(null=False, blank=False)
    block_number = models.PositiveIntegerField(null=False, blank=False)
    is_error = models.BooleanField(default=0)
    to_address = models.CharField(max_length=100, blank=False, null=False)
    from_address = models.CharField(max_length=100, blank=False, null=False)
    volumes = models.TextField(null=True)

    class Meta:
        managed = True
        db_table = 'seaport_transaction'

class Seaport721Transaction(models.Model):

    tx_hash = models.ForeignKey(SeaportTransaction, on_delete=models.DO_NOTHING)
    contract_address = models.CharField(max_length=100, blank=True, null=True)
    token_id = models.CharField(max_length=100, blank=True, null=True)
    matic_price = models.DecimalField( max_digits=65, decimal_places=0)
    usdc_price = models.DecimalField( max_digits=65, decimal_places=0)
    weth_price = models.DecimalField( max_digits=65, decimal_places=0)
    spot_price = models.DecimalField( max_digits=65, decimal_places=0)
    buyer = models.CharField(max_length=100, blank=False, null=False)
    seller = models.CharField(max_length=100, blank=False, null=False)


    class Meta:
        managed = True
        db_table = 'seaport_721_transaction'



class Seaport1155Transaction(models.Model):

    tx_hash = models.ForeignKey(SeaportTransaction, on_delete=models.DO_NOTHING)
    contract_address = models.CharField(max_length=100, blank=True, null=True)
    token_id = models.CharField(max_length=100, blank=True, null=True)
    quantity = models.DecimalField( max_digits=65, decimal_places=0)
    matic_price = models.DecimalField( max_digits=65, decimal_places=0)
    usdc_price = models.DecimalField( max_digits=65, decimal_places=0)
    weth_price = models.DecimalField( max_digits=65, decimal_places=0)
    spot_price = models.DecimalField( max_digits=65, decimal_places=0)
    buyer = models.CharField(max_length=100, blank=False, null=False)
    seller = models.CharField(max_length=100, blank=False, null=False)


    class Meta:
        managed = True
        db_table = 'seaport_1155_transaction'

# price is in dollars per whole coin

class SpotPrice(models.Model):

    token_name = models.CharField(max_length=16, blank=False, null=False)
    price = models.FloatField(null=False)