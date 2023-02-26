from nft.models import SeaportTransaction



from django.core.management.base import BaseCommand
from django.utils import timezone

from web3 import Web3
from polygon.settings import INFURA_RPC_URL, POLYGONSCAN_API_KEY, SEAPORT_CONTRACT_ABI
web3 = Web3(Web3.HTTPProvider(INFURA_RPC_URL))
from web3.middleware import geth_poa_middleware
web3.middleware_onion.inject(geth_poa_middleware, layer=0)

seaport = web3.eth.contract(address="0x00000000006c3852cbEf3e08E8dF289169EdE581", abi=SEAPORT_CONTRACT_ABI)



class Command(BaseCommand):
    help = 'Displays current time'

    def add_arguments(self, parser):
        parser.add_argument('start_block', type=int, help='scrape transactions starting with this Block #')
        parser.add_argument('end_block', type=int, help='Stop Scraping Transactions when this block # is reached')

    def handle(self, *args, **kwargs):
        time = timezone.now().strftime('%X')
        print('start')
        print(kwargs['start_block'])
        print("end")
        print(kwargs['end_block'])
        self.stdout.write("It's now %s" % time)