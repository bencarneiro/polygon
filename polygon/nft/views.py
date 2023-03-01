from django.shortcuts import render
from django.db.models import Q
from datetime import datetime

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from nft.models import SeaportTransaction, Seaport1155Transaction, Seaport721Transaction

# Create your views here.


@csrf_exempt
def get_transactions(request):
    q = Q()

    # these filters are run on the main tx table

    if "start_dt" in request.GET:
        q &= Q(tx_hash__dt__gte=datetime.fromtimestamp(int(request.GET['start_dt'])))
    if "end_dt" in request.GET:
        q &= Q(tx_hash__dt__lte=datetime.fromtimestamp(int(request.GET['end_dt'])))
    if "start_block" in request.GET:
        q &= Q(tx_hash__block_number__gte=request.GET['start_block'])
    if "end_block" in request.GET:
        q &= Q(tx_hash__block_number__lte=request.GET['end_block'])

    # these filters are run on the subtable
    if "buyer" in request.GET:
        y &= Q(buyer=request.GET['buyer'])
    if "seller" in request.GET:
        y &= Q(seller=request.GET['seller'])
    if "contract_address" in request.GET:
         y &= Q(contract_address=request.GET['contract_address'])
    if "token_id" in request.GET:
        y &= Q(token_id=request.GET['token_id'])
    if "coin_standard" in request.GET:
        coin_standard = request.GET['coin_standard']
        if coin_standard not in ['1155', '721']:
            return JsonResponse({'status': 'error', 'message': 'coin_standard is invalid: needs to be 721 or 1155'})
    else:
        coin_standard = "all"

    data721 = Seaport721Transaction.objects.filter(q)
    data1155 = Seaport1155Transaction.objects.filter(q)
    if coin_standard == "all":
        response_data = list(data721.values("tx_hash", "contract_address", "token_id", "buyer", "seller", "matic_price", "weth_price", "usdc_price", "tx_hash__dt", "tx_hash__block_number", "tx_hash__method_name")) + list(data1155.values("tx_hash", "contract_address", "token_id", "quantity", "buyer", "seller", "matic_price", "weth_price", "usdc_price", "tx_hash__dt", "tx_hash__block_number", "tx_hash__method_name"))
    if coin_standard == "721":
        response_data = list(data721.values("tx_hash", "contract_address", "token_id", "buyer", "seller", "matic_price", "weth_price", "usdc_price", "tx_hash__dt", "tx_hash__block_number", "tx_hash__method_name"))
    if coin_standard == "1155":
        response_data = list(data1155.values("tx_hash", "contract_address", "token_id", "quantity", "buyer", "seller", "matic_price", "weth_price", "usdc_price", "tx_hash__dt", "tx_hash__block_number", "tx_hash__method_name"))
    
    response = {
        'length': len(response_data),
        'status': "success",
        "data": response_data
    }
    return JsonResponse(response)
    
    

@csrf_exempt
def get_daily_sales(request):
    q = Q()

    # these filters are run on the main tx table

    if "start_dt" in request.GET:
        q &= Q(tx_hash__dt__gte=datetime.fromtimestamp(int(request.GET['start_dt'])))
    if "end_dt" in request.GET:
        q &= Q(tx_hash__dt__lte=datetime.fromtimestamp(int(request.GET['end_dt'])))
    if "start_block" in request.GET:
        q &= Q(tx_hash__block_number__gte=request.GET['start_block'])
    if "end_block" in request.GET:
        q &= Q(tx_hash__block_number__lte=request.GET['end_block'])

    # these filters are run on the subtable
    if "buyer" in request.GET:
        y &= Q(buyer=request.GET['buyer'])
    if "seller" in request.GET:
        y &= Q(seller=request.GET['seller'])
    if "contract_address" in request.GET:
         y &= Q(contract_address=request.GET['contract_address'])
    if "token_id" in request.GET:
        y &= Q(token_id=request.GET['token_id'])

    data721 = Seaport721Transaction.objects.filter(q)
    data1155 = Seaport1155Transaction.objects.filter(q)
    # usdc_volume
    response = {
        "status": "success",
        "data": []
    }
    return JsonResponse(response)

    # steps
    # take start_dt, end_dt, start_block, end_block
    # segment the total timeframe into its component days by epoch   timestamp (49403394-3940494933)
    # for each of the timeblocks, crunch the numbers on data721 and data1155
    # add each set of stats to the data list in order



    # todo allow for filter by type (721/1155)

    # Structure needs to look like this
    # {"data": [{
    #     "date": "2020-15-15"
    #     "matic_volume":
    #     "weth_volume":
    #     "usdc_volume"
    #     "total volume in current USD"
    #     "number of transactions"
    #     "filter parameters" : {"contract_address": , "token_id"}
    # }]}