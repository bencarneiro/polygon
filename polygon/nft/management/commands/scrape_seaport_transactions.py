from nft.models import SeaportTransaction



from django.core.management.base import BaseCommand
from django.utils import timezone

from web3 import Web3
from polygon.settings import INFURA_RPC_URL, POLYGONSCAN_API_KEY, SEAPORT_CONTRACT_ABI, SEAPORT_ADDRESS
web3 = Web3(Web3.HTTPProvider(INFURA_RPC_URL))
from web3.middleware import geth_poa_middleware
web3.middleware_onion.inject(geth_poa_middleware, layer=0)
from nft.models import SeaportTransaction
from datetime import datetime

import requests

seaport = web3.eth.contract(address="0x00000000006c3852cbEf3e08E8dF289169EdE581", abi=SEAPORT_CONTRACT_ABI)


# here is an example of someone doing this for a twitter bot in js
# https://github.com/dsgriffin/nft-sales-twitter-bot/blob/master/app.js

def determine_volumes(tx_hash):
    # random trump transaction

    rct = web3.eth.get_transaction_receipt(tx_hash)
    transfers = {}
    for log in rct['logs']:
        if web3.toHex(log['topics'][0]) == "0xe6497e3ee548a3372136af2fcb0696db31fc6cf20260707645068bd3fe97f3c4":
            if not "matic" in transfers:
                transfers['matic'] = web3.toInt(hexstr=log['data'][2:66])
            elif web3.toInt(hexstr=log['data'][2:66]) > transfers['matic']:
                transfers['matic'] = web3.toInt(hexstr=log['data'][2:66])
        if web3.toHex(log['topics'][0]) == "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef":
            if len(log['topics']) == 4:
                if log['address'] not in transfers:
                    transfers[log['address']] = [web3.toInt(log['topics'][3])]
                else:
                    transfers[log['address']] += [web3.toInt(log['topics'][3])]
            if len(log['topics']) == 3:
                if log['address'] not in transfers:
                    transfers[log['address']] = web3.toInt(hexstr=log['data'][2:66])
                elif web3.toInt(hexstr=log['data'][2:66]) > transfers[log['address']]:
                    transfers[log['address']] = web3.toInt(hexstr=log['data'][2:66])
        if web3.toHex(log['topics'][0]) == "0xc3d58168c5ae7397731d063d5bbf3d657854427343f4c083240f7aacaa2d0f62":
            if log['address'] not in transfers:
                transfers[log['address']] = [(web3.toInt(hexstr=log['data'][2:66]), web3.toInt(hexstr=log['data'][66:130]))]
            else: 
                transfers[log['address']] += [(web3.toInt(hexstr=log['data'][2:66]), web3.toInt(hexstr=log['data'][66:130]))]
    return transfers
 

class Command(BaseCommand):
    help = 'Displays current time'

    def add_arguments(self, parser):
        parser.add_argument('start_block', type=int, help='scrape transactions starting with this Block #')
        parser.add_argument('end_block', type=int, help='Stop Scraping Transactions when this block # is reached')

    def handle(self, *args, **kwargs):
        page = 1
        more = True
        while more:
            polygon_scan_url = f"https://api.polygonscan.com/api?module=account&action=txlist&address={SEAPORT_ADDRESS}&startblock={kwargs['start_block']}&endblock={kwargs['end_block']}&page={page}&offset=1000&sort=asc&apikey={POLYGONSCAN_API_KEY}"
            resp = requests.get(polygon_scan_url)
            seaport_txs = resp.json()
            print(seaport_txs)
            for tx in seaport_txs['result']:
                print(tx['functionName'])
                if tx['functionName'] == "fulfillBasicOrder(tuple)": 
                    print(tx)
                    function_input_params = seaport.decode_function_input(tx['input'])[1]['parameters']
                    token_contract_address = function_input_params[5]
                    token_id = function_input_params[6]
                    tx_volumes = determine_volumes(tx['hash'])
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
                        tx_input=tx['input'],
                        volumes=tx_volumes
                    )
                    new_tx.save()
                else:
                    tx_volumes = determine_volumes(tx['hash'])
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
                        tx_input=tx['input'],
                        volumes=tx_volumes
                    )
                    new_tx.save()
            if len(seaport_txs['result']) == 1000:
                more = True
                page += 1
            else:
                more = False
        
        # time = timezone.now().strftime('%X')
        # print('start')
        # print(kwargs['start_block'])
        # print("end")
        # print(kwargs['end_block'])
        # self.stdout.write("It's now %s" % time)