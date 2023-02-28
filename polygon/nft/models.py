from django.db import models

# Create your models here.

class SeaportTransaction(models.Model):

    tx_hash = models.CharField(max_length=100, blank=False, null=False)
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

    tx_hash = models.CharField(max_length=100, blank=False, null=False)
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

    tx_hash = models.CharField(max_length=100, blank=False, null=False)
    contract_address = models.CharField(max_length=100, blank=True, null=True)
    token_id = models.CharField(max_length=100, blank=True, null=True)
    quantity = models.BigIntegerField(blank=False, null=False)
    matic_price = models.DecimalField( max_digits=65, decimal_places=0)
    usdc_price = models.DecimalField( max_digits=65, decimal_places=0)
    weth_price = models.DecimalField( max_digits=65, decimal_places=0)
    spot_price = models.DecimalField( max_digits=65, decimal_places=0)
    buyer = models.CharField(max_length=100, blank=False, null=False)
    seller = models.CharField(max_length=100, blank=False, null=False)


    class Meta:
        managed = True
        db_table = 'seaport_1155_transaction'


# {'blockNumber': '29701456',
#  'timeStamp': '1655526125',
#  'hash': '0xc43e98c8f615f557123306c50e8b0c6d490b1a5ef5bc2dde5583c2daec04f3c7',
#  'nonce': '14',
#  'blockHash': '0x50b7bb84c584e49be95adfad559b1beff6f6700b5116542bfed0088abbefb027',
#  'transactionIndex': '64',
#  'from': '0xbfb4450ba63d6858aaf5dd48c1516e559cfe9439',
#  'to': '0x00000000006c3852cbef3e08e8df289169ede581',
#  'value': '16799900000000000',
#  'gas': '151376',
#  'gasPrice': '30153097551',
#  'isError': '0',
#  'txreceipt_status': '1',
#  'input': '0xfb0f3ee10000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000035b77a6095fc00000000000000000000000000cac8ca2c41b14304906c884db9603a7b29d98adb000000000000000000000000004c00500000ad104d7dbd00e3ae0a5c00560c00000000000000000000000000e3d0fe9b7e0b951663267a3ed1e6577f6f79757e0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000070000000000000000000000000000000000000000000000000000000062ad1fa00000000000000000000000000000000000000000000000000000000062ae71200000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000007c4dcfd274d3660000007b02230091a7ed01230072f7006a004d60a8d4e71d599b8104250f00000000007b02230091a7ed01230072f7006a004d60a8d4e71d599b8104250f00000000000000000000000000000000000000000000000000000000000000000002000000000000000000000000000000000000000000000000000000000000024000000000000000000000000000000000000000000000000000000000000002e0000000000000000000000000000000000000000000000000000000000000000200000000000000000000000000000000000000000000000000017dfc49cb47000000000000000000000000008de9c5a032463c561423387a9648c5c7bcc5bc90000000000000000000000000000000000000000000000000000479f4dd61d5000000000000000000000000008914496dc01efcc49a2fa340331fb90969b6f1d2000000000000000000000000000000000000000000000000000000000000004106f59712114c59dedbfa77f860acb0841fdc871025470246efa0fbfa8671f38c58afb7cffd440ecc81ded64aeededeae77de3c4e7d7231384a9460462730d64f1b00000000000000000000000000000000000000000000000000000000000000',
#  'contractAddress': '',
#  'cumulativeGasUsed': '8682092',
#  'gasUsed': '27612',
#  'confirmations': '10038705',
#  'methodId': '0xfb0f3ee1',
#  'functionName': 'fulfillBasicOrder(tuple)'}


#  AttributeDict({'accessList': [],
#  'blockHash': HexBytes('0x059bfd2956bab53c63ed99f0d9628872dda6fb18a06d505c5f4b210824bb547e'),
#  'blockNumber': 39640160,
#  'chainId': '0x89',
#  'from': '0xBC6518D2463e52Ce89d5e37f55438e953Fa12211',
#  'gas': 282105,
#  'gasPrice': 157432052708,
#  'hash': HexBytes('0x6cd59a39d8297c67f56bb3ee9ff3918fa173051334b966cc1b5d7dce6c7c5f54'),
#  'input': '0xfb0f3ee100000000000000000000000000000000000000000000000000000000000000200000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000032593ec72d1e00000000000000000000000000003ebaf00176a77a9ede760dc43f798a9ad2a87c8a000000000000000000000000000000000000000000000000000000000000000000000000000000000000000019fbb5e802b58e5fd1b6de259a2f044b478550a400000000000000000000000000000000000000000000000000000000000002eb000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000063f7c23600000000000000000000000000000000000000000000000000000000641cac360000000000000000000000000000000000000000000000000000000000000000360c6ebe0000000000000000000000000000000000000000ae48d6804fe4273f0000007b02230091a7ed01230072f7006a004d60a8d4e71d599b8104250f00000000007b02230091a7ed01230072f7006a004d60a8d4e71d599b8104250f0000000000000000000000000000000000000000000000000000000000000000000300000000000000000000000000000000000000000000000000000000000002400000000000000000000000000000000000000000000000000000000000000320000000000000000000000000000000000000000000000000000000000000000300000000000000000000000000000000000000000000000000470de4df8200000000000000000000000000000000a26b00c1f0df003000390027140000faa7190000000000000000000000000000000000000000000000000271471148780000000000000000000000000000779f1fdbad89be2c97e6abf1603d3b0dddc657dd000000000000000000000000000000000000000000000000027147114878000000000000000000000000000056772fb0c956297454acebb435f90f69e30ee9d50000000000000000000000000000000000000000000000000000000000000041274cbdbde6722a6edd087bb9b3e0618ce226096e5acc25d35c16d19c506fc8e466460d3ae1b3ba9f5852de245dfa132ede7c1eecf0524944a7638a64d5b4169a1c0000000000000000000000000000000000000000000000000000000000000000000000360c6ebe',
#  'maxFeePerGas': 196846723200,
#  'maxPriorityFeePerGas': 30000000000,
#  'nonce': 0,
#  'r': HexBytes('0x34305d0bfe52c16605eb6bad8c0811a902450793121bcad369cfcf362a5dafed'),
#  's': HexBytes('0x7d581fe94f1158d56cca022ff83f233e9e11113a1f324eeb5d6b7a753ebdbfdc'),
#  'to': '0x00000000006c3852cbEf3e08E8dF289169EdE581',
#  'transactionIndex': 61,
#  'type': '0x2',
#  'v': 0,
#  'value': 4000000000000000000})

 