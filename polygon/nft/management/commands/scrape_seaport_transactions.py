from nft.models import SeaportTransaction



from django.core.management.base import BaseCommand
from django.utils import timezone

from web3 import Web3
from polygon.settings import INFURA_RPC_URL, POLYGONSCAN_API_KEY, SEAPORT_CONTRACT_ABI, SEAPORT_ADDRESS
web3 = Web3(Web3.HTTPProvider(INFURA_RPC_URL))
from web3.middleware import geth_poa_middleware
web3.middleware_onion.inject(geth_poa_middleware, layer=0)
from nft.models import SeaportTransaction, Seaport1155Transaction, Seaport721Transaction
from datetime import datetime

import requests

seaport = web3.eth.contract(address="0x00000000006c3852cbEf3e08E8dF289169EdE581", abi=SEAPORT_CONTRACT_ABI)


# here is an example of someone doing this for a twitter bot in js
# https://github.com/dsgriffin/nft-sales-twitter-bot/blob/master/app.js

def determine_volumes(tx_hash):
    rct = web3.eth.get_transaction_receipt(tx_hash)
    transfers = []
    for log in rct['logs']:
        if web3.toHex(log['topics'][0]) == "0xe6497e3ee548a3372136af2fcb0696db31fc6cf20260707645068bd3fe97f3c4":
            tx = {"type": "MATIC", 'from': "0x" + str(web3.toHex(log['topics'][2])[26:]), 'to': "0x" + str(web3.toHex(log['topics'][3])[26:]), "amount": web3.toInt(hexstr=log['data'][2:66])}
            transfers += [tx]
        if web3.toHex(log['topics'][0]) == "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef":
            if len(log['topics']) == 4:
                tx = {"type": "ERC721", "from": "0x" + str(web3.toHex(log['topics'][1]))[26:], "to": "0x" + str(web3.toHex(log['topics'][2]))[26:], "contract_address": log['address'], "token_id": web3.toInt(log['topics'][3])}
                transfers += [tx]
            if len(log['topics']) == 3:
                if log['address'] == "0x7ceB23fD6bC0adD59E62ac25578270cFf1b9f619":
                    tx = {'type': "WETH", "from": "0x" + str(web3.toHex(log['topics'][1]))[26:], "to": "0x" + str(web3.toHex(log['topics'][2]))[26:], "amount": web3.toInt(hexstr=log['data'][2:66])}
                elif log['address'] == "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174":
                    tx = {'type': "USDC", "from": "0x" + str(web3.toHex(log['topics'][1]))[26:], "to": "0x" + str(web3.toHex(log['topics'][2]))[26:], "amount": web3.toInt(hexstr=log['data'][2:66])}
                else:
                    tx = {'type': "ERC20", "from": "0x" + str(web3.toHex(log['topics'][1]))[26:], "to": "0x" + str(web3.toHex(log['topics'][2]))[26:], "amount": web3.toInt(hexstr=log['data'][2:66]), 'contract_address': log['address']}
                transfers += [tx]
        if web3.toHex(log['topics'][0]) == "0xc3d58168c5ae7397731d063d5bbf3d657854427343f4c083240f7aacaa2d0f62":
            tx = {"type": "ERC1155", "from": "0x" + str(web3.toHex(log['topics'][2]))[26:], 'to': "0x" + str(web3.toHex(log['topics'][3]))[26:], "contract_address": log['address'], 'token_id': web3.toInt(hexstr=log['data'][2:66]), 'quantity': web3.toInt(hexstr=log['data'][66:130])}
            transfers += [tx]
    return transfers

def analyze_volumes(tx, transfers):
    buyer = None
    # print(transfers)
    nft_transfers_by_sender = {}
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
        volumes=transfers
    )
    new_tx.save()

    for transfer in transfers:

        if (transfer['type'] == "ERC721") or (transfer['type'] == "ERC1155"):
            if transfer['from'] not in nft_transfers_by_sender:
                nft_transfers_by_sender[transfer['from']] = {'nfts': [transfer], 'coins': []}
            else:
                nft_transfers_by_sender[transfer['from']]['nfts'] += [transfer]

        if transfer['type'] in ['MATIC', "WETH", 'USDC']:
            if transfer['to'] not in nft_transfers_by_sender:
                nft_transfers_by_sender[transfer['to']] = {'nfts': [], 'coins': [transfer]}
            else:
                nft_transfers_by_sender[transfer['to']]['coins'] += [transfer]

    # print(nft_transfers_by_sender)
    for seller_address in nft_transfers_by_sender:

        # print(nft_transfers_by_sender[seller_address])
        trading_activity = nft_transfers_by_sender[seller_address]

        if len(trading_activity['coins']) > 0 and len(trading_activity['nfts']) > 0:

            matic_price = 0
            usdc_price = 0
            weth_price = 0
            spot_price = 0

            for coin_transfer in trading_activity['coins']:
                if coin_transfer['type'] == "MATIC":
                    matic_price = coin_transfer['amount'] / len(trading_activity['nfts'])
                if coin_transfer['type'] == "USDC":
                    usdc_price = coin_transfer['amount'] / len(trading_activity['nfts'])
                if coin_transfer['type'] == "WETH":
                    weth_price = coin_transfer['amount'] / len(trading_activity['nfts'])

            for nft_transfer in trading_activity['nfts']:
                if nft_transfer['type'] == "ERC721":
                    new_721_tx = Seaport721Transaction(
                        tx_hash = new_tx,
                        contract_address = nft_transfer['contract_address'],
                        token_id = nft_transfer['token_id'],
                        matic_price = matic_price,
                        usdc_price = usdc_price,
                        weth_price = weth_price,
                        spot_price = spot_price,
                        buyer = nft_transfer['to'],
                        seller = seller_address
                    )
                    new_721_tx.save()

                if nft_transfer['type'] == "ERC1155":
                    new_1155_tx = Seaport1155Transaction(
                        tx_hash = new_tx,
                        contract_address = nft_transfer['contract_address'],
                        token_id = nft_transfer['token_id'],
                        quantity = nft_transfer['quantity'],
                        matic_price = matic_price,
                        usdc_price = usdc_price,
                        weth_price = weth_price,
                        spot_price = spot_price,
                        buyer = nft_transfer['to'],
                        seller = seller_address
                    )
                    new_1155_tx.save()



class Command(BaseCommand):
    help = 'Displays current time'

    def add_arguments(self, parser):
        parser.add_argument('start_block', type=int, help='scrape transactions starting with this Block #')
        parser.add_argument('end_block', type=int, help='Stop Scraping Transactions when this block # is reached')

    def handle(self, *args, **kwargs):
        page = 1
        more = True
        # todo fix this logic to change API call start and end block instead of trying to paginate on the one request
        # can only fetch 10K results- Need to change start and end block to comb more than 10K txs
        start_block = kwargs['start_block']
        end_block = kwargs['end_block']
        while more:
            print(f"making new request from blocks {start_block} to {end_block}")
            polygon_scan_url = f"https://api.polygonscan.com/api?module=account&action=txlist&address={SEAPORT_ADDRESS}&startblock={start_block}&endblock={end_block}&page={page}&offset=10000&sort=asc&apikey={POLYGONSCAN_API_KEY}"
            resp = requests.get(polygon_scan_url)
            seaport_txs = resp.json()
            for tx in seaport_txs['result']:
                try:
                    tx_volumes = determine_volumes(tx['hash'])
                    analyze_volumes(tx, tx_volumes)
                    print(f"successfully analyzed tx_hash {tx['hash']}")
                except Exception as e: 
                    print("SOMETHING WENT WRONG")
                    print(e)
                    print(tx)
            if len(seaport_txs['result']) == 10000:
                more = True
                start_block = str(seaport_txs['result'][-1]['blockNumber'])
            else:
                more = False
        
        # time = timezone.now().strftime('%X')
        # print('start')
        # print(kwargs['start_block'])
        # print("end")
        # print(kwargs['end_block'])
        # self.stdout.write("It's now %s" % time)