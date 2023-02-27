from nft.models import SeaportTransaction



from django.core.management.base import BaseCommand
from django.utils import timezone

from web3 import Web3
from polygon.settings import INFURA_RPC_URL, POLYGONSCAN_API_KEY, SEAPORT_CONTRACT_ABI
web3 = Web3(Web3.HTTPProvider(INFURA_RPC_URL))
from web3.middleware import geth_poa_middleware
web3.middleware_onion.inject(geth_poa_middleware, layer=0)
from nft.models import SeaportTransaction
from datetime import datetime

import requests

seaport = web3.eth.contract(address="0x00000000006c3852cbEf3e08E8dF289169EdE581", abi=SEAPORT_CONTRACT_ABI)



class Command(BaseCommand):
    help = 'Displays current time'

    def add_arguments(self, parser):
        parser.add_argument('start_block', type=int, help='scrape transactions starting with this Block #')
        parser.add_argument('end_block', type=int, help='Stop Scraping Transactions when this block # is reached')

    def handle(self, *args, **kwargs):
        resp = requests.get('https://api.polygonscan.com/api?module=account&action=txlist&address=0x00000000006c3852cbEf3e08E8dF289169EdE581&startblock=0&endblock=99999999&page=1&offset=10&sort=asc&apikey=CC75ZX7TC9GHD7IC3NF6S222GHCYREI1CJ')
        seaport_txs = resp.json()
        for tx in seaport_txs['result']:
            if tx['functionName'] == "fulfillBasicOrder(tuple)": 
                print(tx)
                function_input_params = seaport.decode_function_input(tx['input'])[1]['parameters']
                token_contract_address = function_input_params[5]
                token_id = function_input_params[6]
                new_tx = SeaportTransaction(
                    tx_hash = tx['hash'],
                    method_name = tx['functionName'],
                    value = tx['value'],
                    gas_price = int(tx['gasPrice']),
                    gas_used = int(tx['gasUsed']),
                    tx_fee = int(tx['gasUsed']) * int(tx['gasPrice']),
                    tx_reciept_status = tx['txreceipt_status'],
                    dt = datetime.fromtimestamp(int(tx['timeStamp'])),
                    block_number = tx['blockNumber'],
                    is_error = tx['isError'],
                    to_address = tx['to'],
                    from_address = tx['from'],
                    token_contract_address = token_contract_address,
                    token_id = token_id,
                    tx_input=tx['input']
                )
                new_tx.save()
        # time = timezone.now().strftime('%X')
        # print('start')
        # print(kwargs['start_block'])
        # print("end")
        # print(kwargs['end_block'])
        # self.stdout.write("It's now %s" % time)