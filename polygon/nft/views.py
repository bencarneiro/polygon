from django.shortcuts import render
from django.db.models import Q, FloatField
from datetime import datetime
from django.db.models.functions import TruncMonth, TruncDay, TruncYear, TruncWeek
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from nft.models import SeaportTransaction, Seaport1155Transaction, Seaport721Transaction, SpotPrice
from django.db.models import Sum, Count

# Create your views here.


@csrf_exempt
def get_transactions(request):
    q = Q()
    params = {}
    # these filters are run on the main tx table

    if "start_dt" in request.GET:
        params['start_dt'] = request.GET['start_dt']
        q &= Q(tx_hash__dt__gte=datetime.fromtimestamp(int(request.GET['start_dt'])))
    if "end_dt" in request.GET:
        params['end_dt'] = request.GET['end_dt']
        q &= Q(tx_hash__dt__lte=datetime.fromtimestamp(int(request.GET['end_dt'])))
    if "start_block" in request.GET:
        params['start_block'] = request.GET['start_block']
        q &= Q(tx_hash__block_number__gte=request.GET['start_block'])
    if "end_block" in request.GET:
        params['end_block'] = request.GET['end_block']
        q &= Q(tx_hash__block_number__lte=request.GET['end_block'])

    # these filters are run on the subtable
    if "buyer" in request.GET:
        params['buyer'] = request.GET['buyer']
        q &= Q(buyer=request.GET['buyer'])
    if "seller" in request.GET:
        params['seller'] = request.GET['seller']
        q &= Q(seller=request.GET['seller'])
    if "contract_address" in request.GET:
        params['contract_address'] = request.GET['contract_address']
        q &= Q(contract_address=request.GET['contract_address'])
    if "token_id" in request.GET:
        params['token_id'] = request.GET['token_id']
        q &= Q(token_id=request.GET['token_id'])
    if "coin_standard" in request.GET:
        params['coin_standard'] = request.GET['coin_standard']
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
        "data": response_data,
        'parameters': params
    }
    return JsonResponse(response)
    
    

@csrf_exempt
def get_volume(request):
    q = Q()

    # these filters are run on the main tx table
    params = {}
    if "start_dt" in request.GET:
        params['start_dt'] = request.GET['start_dt']
        q &= Q(tx_hash__dt__gte=datetime.fromtimestamp(int(request.GET['start_dt'])))
    if "end_dt" in request.GET:
        q &= Q(tx_hash__dt__lte=datetime.fromtimestamp(int(request.GET['end_dt'])))
        params['end_dt'] = request.GET['end_dt']
    # if "start_block" in request.GET:
    #     q &= Q(tx_hash__block_number__gte=request.GET['start_block'])
    # if "end_block" in request.GET:
    #     q &= Q(tx_hash__block_number__lte=request.GET['end_block'])

    # these filters are run on the subtable
    if "buyer" in request.GET:
        q &= Q(buyer=request.GET['buyer'])
        params['buyer'] = request.GET['buyer']
    if "seller" in request.GET:
        q &= Q(seller=request.GET['seller'])
        params['seller'] = request.GET['seller']
    if "contract_address" in request.GET:
         q &= Q(contract_address=request.GET['contract_address'])
         params['contract_address'] = request.GET['contract_address']
    if "token_id" in request.GET:
        q &= Q(token_id=request.GET['token_id'])
        params['token_id'] = request.GET['token_id']
    if "coin_standard" in request.GET:
        params['coin_standard'] = request.GET['coin_standard']
        coin_standard = request.GET['coin_standard']
        if coin_standard not in ['1155', '721']:
            return JsonResponse({'status': 'error', 'message': 'coin_standard is invalid: needs to be 721 or 1155'})
    else:
        coin_standard = "all"


    data721 = Seaport721Transaction.objects.filter(q)
    data1155 = Seaport1155Transaction.objects.filter(q)

    nft_volumes_721 = data721.aggregate(matic_volume=Sum("matic_price"), usdc_volume=Sum("usdc_price"), weth_volume=Sum('weth_price'), total_transactions=Count('id'))
    nft_volumes_1155 = data1155.aggregate(matic_volume=Sum("matic_price"), usdc_volume=Sum("usdc_price"), weth_volume=Sum('weth_price'), total_transactions=Count('id'))
    if coin_standard == "all":
        total_volumes = {
            "matic_volume": int(nft_volumes_721['matic_volume'])/(10**18) + int(nft_volumes_1155['matic_volume'])/(10**18),
            "usdc_volume": int(nft_volumes_721['usdc_volume'])/(10**6) + int(nft_volumes_1155['usdc_volume'])/(10**6),
            "weth_volume": int(nft_volumes_721['weth_volume'])/(10**18) + int(nft_volumes_1155['weth_volume'])/(10**18),
            "tx_count": int(nft_volumes_721['total_transactions']) + int(nft_volumes_1155['total_transactions'])
        }
    if coin_standard == "721":
        total_volumes = {
            "matic_volume": int(nft_volumes_721['matic_volume'])/(10**18),
            "usdc_volume": int(nft_volumes_721['usdc_volume'])/(10**6),
            "weth_volume": int(nft_volumes_721['weth_volume'])/(10**18),
            "tx_count": int(nft_volumes_721['total_transactions'])
        }
    if coin_standard == "1155":
        total_volumes = {
            "matic_volume":int(nft_volumes_1155['matic_volume'])/(10**18),
            "usdc_volume": int(nft_volumes_1155['usdc_volume'])/(10**6),
            "weth_volume": int(nft_volumes_1155['weth_volume'])/(10**18),
            "tx_count": int(nft_volumes_1155['total_transactions'])
        }
    # usdc_volume
    response = {
        "status": "success",
        "data": total_volumes,
        "parameters": params
    }
    return JsonResponse(response)

    # steps
    # take start_dt, end_dt, start_block, end_block
    # segment the total timeframe into its component days by epoch   timestamp (49403394-3940494933)
    # for each of the timeblocks, crunch the numbers on data721 and data1155
    # add each set of stats to the data list in order



@csrf_exempt
def get_daily_sales_volume(request):
    q = Q()

    # these filters are run on the main tx table
    params = {}
    if "start_dt" in request.GET:
        params['start_dt'] = request.GET['start_dt']
        q &= Q(tx_hash__dt__gte=datetime.fromtimestamp(int(request.GET['start_dt'])))
    if "end_dt" in request.GET:
        q &= Q(tx_hash__dt__lte=datetime.fromtimestamp(int(request.GET['end_dt'])))
        params['end_dt'] = request.GET['end_dt']
    # if "start_block" in request.GET:
    #     q &= Q(tx_hash__block_number__gte=request.GET['start_block'])
    # if "end_block" in request.GET:
    #     q &= Q(tx_hash__block_number__lte=request.GET['end_block'])

    # these filters are run on the subtable
    if "buyer" in request.GET:
        q &= Q(buyer=request.GET['buyer'])
        params['buyer'] = request.GET['buyer']
    if "seller" in request.GET:
        q &= Q(seller=request.GET['seller'])
        params['seller'] = request.GET['seller']
    if "contract_address" in request.GET:
         q &= Q(contract_address=request.GET['contract_address'])
         params['contract_address'] = request.GET['contract_address']
    if "token_id" in request.GET:
        q &= Q(token_id=request.GET['token_id'])
        params['token_id'] = request.GET['token_id']
    if "coin_standard" in request.GET:
        params['coin_standard'] = request.GET['coin_standard']
        coin_standard = request.GET['coin_standard']
        if coin_standard not in ['1155', '721']:
            return JsonResponse({'status': 'error', 'message': 'coin_standard is invalid: needs to be 721 or 1155'})
    else:
        coin_standard = "all"


    data721 = Seaport721Transaction.objects.filter(q)
    data1155 = Seaport1155Transaction.objects.filter(q)

    # nft_volumes_721 = data721.annotate(matic_volume=Sum("matic_price"), usdc_volume=Sum("usdc_price"), weth_volume=Sum('weth_price'), total_transactions=Count('id'))
    # nft_volumes_1155 = data1155.aggregate(matic_volume=Sum("matic_price"), usdc_volume=Sum("usdc_price"), weth_volume=Sum('weth_price'), total_transactions=Count('id'))

    matic_spot_price = SpotPrice.objects.get(token_name="MATIC").price
    weth_spot_price = SpotPrice.objects.get(token_name="WETH").price
    usdc_spot_price = 1

    daily_sales_721 = Seaport721Transaction.objects.filter(q).annotate(
        day=TruncDay('tx_hash__dt'),
    ).values('day').annotate(
        matic_volume=(Sum('matic_price')/(10**18)),
        usdc_volume=(Sum('usdc_price')/(10**6)),
        weth_volume=(Sum('weth_price')/(10**18)),
        total_sales=(Count('id')),
        spot_usd_volume=((Sum('matic_price', output_field=FloatField())/(10**18))*matic_spot_price) + ((Sum('usdc_price', output_field=FloatField())/(10**6))) + ((Sum('weth_price', output_field=FloatField())/(10**18))*weth_spot_price),
        average_sale_price=(((Sum('matic_price', output_field=FloatField())/(10**18))*matic_spot_price) + ((Sum('usdc_price', output_field=FloatField())/(10**6))) + ((Sum('weth_price', output_field=FloatField())/(10**18))*weth_spot_price)) / (Count('id'))
    )

    daily_sales_1155 = Seaport1155Transaction.objects.filter(q).annotate(
        day=TruncDay('tx_hash__dt'),
    ).values('day').annotate(
        matic_volume=(Sum('matic_price')/(10**18)),
        usdc_volume=(Sum('usdc_price')/(10**6)),
        weth_volume=(Sum('weth_price')/(10**18)),
        total_sales=(Count('id')),
        total_individual_tokens_sold=Sum("quantity"),
        spot_usd_volume=((Sum('matic_price', output_field=FloatField())/(10**18))*matic_spot_price) + ((Sum('usdc_price', output_field=FloatField())/(10**6))) + ((Sum('weth_price', output_field=FloatField())/(10**18))*weth_spot_price),
        average_sale_price=(((Sum('matic_price', output_field=FloatField())/(10**18))*matic_spot_price) + ((Sum('usdc_price', output_field=FloatField())/(10**6))) + ((Sum('weth_price', output_field=FloatField())/(10**18))*weth_spot_price)) / (Count('id')),
        average_sale_price_per_individual_token=(((Sum('matic_price', output_field=FloatField())/(10**18))*matic_spot_price) + ((Sum('usdc_price', output_field=FloatField())/(10**6))) + ((Sum('weth_price', output_field=FloatField())/(10**18))*weth_spot_price)) / (Sum('quantity', output_field=FloatField()))
    )

    response = {
        "status": "success",
        "data": {
            "721": list(daily_sales_721),
            "1155": list(daily_sales_1155)
        },
        "parameters": params
    }

    return JsonResponse(response)



@csrf_exempt
def get_weekly_sales_volume(request):
    q = Q()

    # these filters are run on the main tx table
    params = {}
    if "start_dt" in request.GET:
        params['start_dt'] = request.GET['start_dt']
        q &= Q(tx_hash__dt__gte=datetime.fromtimestamp(int(request.GET['start_dt'])))
    if "end_dt" in request.GET:
        q &= Q(tx_hash__dt__lte=datetime.fromtimestamp(int(request.GET['end_dt'])))
        params['end_dt'] = request.GET['end_dt']
    # if "start_block" in request.GET:
    #     q &= Q(tx_hash__block_number__gte=request.GET['start_block'])
    # if "end_block" in request.GET:
    #     q &= Q(tx_hash__block_number__lte=request.GET['end_block'])

    # these filters are run on the subtable
    if "buyer" in request.GET:
        q &= Q(buyer=request.GET['buyer'])
        params['buyer'] = request.GET['buyer']
    if "seller" in request.GET:
        q &= Q(seller=request.GET['seller'])
        params['seller'] = request.GET['seller']
    if "contract_address" in request.GET:
         q &= Q(contract_address=request.GET['contract_address'])
         params['contract_address'] = request.GET['contract_address']
    if "token_id" in request.GET:
        q &= Q(token_id=request.GET['token_id'])
        params['token_id'] = request.GET['token_id']
    if "coin_standard" in request.GET:
        params['coin_standard'] = request.GET['coin_standard']
        coin_standard = request.GET['coin_standard']
        if coin_standard not in ['1155', '721']:
            return JsonResponse({'status': 'error', 'message': 'coin_standard is invalid: needs to be 721 or 1155'})
    else:
        coin_standard = "all"


    data721 = Seaport721Transaction.objects.filter(q)
    data1155 = Seaport1155Transaction.objects.filter(q)

    # nft_volumes_721 = data721.annotate(matic_volume=Sum("matic_price"), usdc_volume=Sum("usdc_price"), weth_volume=Sum('weth_price'), total_transactions=Count('id'))
    # nft_volumes_1155 = data1155.aggregate(matic_volume=Sum("matic_price"), usdc_volume=Sum("usdc_price"), weth_volume=Sum('weth_price'), total_transactions=Count('id'))

    matic_spot_price = SpotPrice.objects.get(token_name="MATIC").price
    weth_spot_price = SpotPrice.objects.get(token_name="WETH").price
    usdc_spot_price = 1

    weekly_sales_721 = Seaport721Transaction.objects.filter(q).annotate(
        week=TruncWeek('tx_hash__dt'),
    ).values('week').annotate(
        matic_volume=(Sum('matic_price')/(10**18)),
        usdc_volume=(Sum('usdc_price')/(10**6)),
        weth_volume=(Sum('weth_price')/(10**18)),
        total_sales=(Count('id')),
        spot_usd_volume=((Sum('matic_price', output_field=FloatField())/(10**18))*matic_spot_price) + ((Sum('usdc_price', output_field=FloatField())/(10**6))) + ((Sum('weth_price', output_field=FloatField())/(10**18))*weth_spot_price),
        average_sale_price=(((Sum('matic_price', output_field=FloatField())/(10**18))*matic_spot_price) + ((Sum('usdc_price', output_field=FloatField())/(10**6))) + ((Sum('weth_price', output_field=FloatField())/(10**18))*weth_spot_price)) / (Count('id'))
    )

    weekly_sales_1155 = Seaport1155Transaction.objects.filter(q).annotate(
        week=TruncWeek('tx_hash__dt'),
    ).values('week').annotate(
        matic_volume=(Sum('matic_price')/(10**18)),
        usdc_volume=(Sum('usdc_price')/(10**6)),
        weth_volume=(Sum('weth_price')/(10**18)),
        total_sales=(Count('id')),
        total_individual_tokens_sold=Sum("quantity"),
        spot_usd_volume=((Sum('matic_price', output_field=FloatField())/(10**18))*matic_spot_price) + ((Sum('usdc_price', output_field=FloatField())/(10**6))) + ((Sum('weth_price', output_field=FloatField())/(10**18))*weth_spot_price),
        average_sale_price=(((Sum('matic_price', output_field=FloatField())/(10**18))*matic_spot_price) + ((Sum('usdc_price', output_field=FloatField())/(10**6))) + ((Sum('weth_price', output_field=FloatField())/(10**18))*weth_spot_price)) / (Count('id')),
        average_sale_price_per_individual_token=(((Sum('matic_price', output_field=FloatField())/(10**18))*matic_spot_price) + ((Sum('usdc_price', output_field=FloatField())/(10**6))) + ((Sum('weth_price', output_field=FloatField())/(10**18))*weth_spot_price)) / (Sum('quantity', output_field=FloatField()))
    )

    response = {
        "status": "success",
        "data": {
            "721": list(weekly_sales_721),
            "1155": list(weekly_sales_1155)
        },
        "parameters": params
    }

    return JsonResponse(response)




@csrf_exempt
def get_monthly_sales_volume(request):
    q = Q()

    # these filters are run on the main tx table
    params = {}
    if "start_dt" in request.GET:
        params['start_dt'] = request.GET['start_dt']
        q &= Q(tx_hash__dt__gte=datetime.fromtimestamp(int(request.GET['start_dt'])))
    if "end_dt" in request.GET:
        q &= Q(tx_hash__dt__lte=datetime.fromtimestamp(int(request.GET['end_dt'])))
        params['end_dt'] = request.GET['end_dt']
    # if "start_block" in request.GET:
    #     q &= Q(tx_hash__block_number__gte=request.GET['start_block'])
    # if "end_block" in request.GET:
    #     q &= Q(tx_hash__block_number__lte=request.GET['end_block'])

    # these filters are run on the subtable
    if "buyer" in request.GET:
        q &= Q(buyer=request.GET['buyer'])
        params['buyer'] = request.GET['buyer']
    if "seller" in request.GET:
        q &= Q(seller=request.GET['seller'])
        params['seller'] = request.GET['seller']
    if "contract_address" in request.GET:
         q &= Q(contract_address=request.GET['contract_address'])
         params['contract_address'] = request.GET['contract_address']
    if "token_id" in request.GET:
        q &= Q(token_id=request.GET['token_id'])
        params['token_id'] = request.GET['token_id']
    if "coin_standard" in request.GET:
        params['coin_standard'] = request.GET['coin_standard']
        coin_standard = request.GET['coin_standard']
        if coin_standard not in ['1155', '721']:
            return JsonResponse({'status': 'error', 'message': 'coin_standard is invalid: needs to be 721 or 1155'})
    else:
        coin_standard = "all"


    data721 = Seaport721Transaction.objects.filter(q)
    data1155 = Seaport1155Transaction.objects.filter(q)

    # nft_volumes_721 = data721.annotate(matic_volume=Sum("matic_price"), usdc_volume=Sum("usdc_price"), weth_volume=Sum('weth_price'), total_transactions=Count('id'))
    # nft_volumes_1155 = data1155.aggregate(matic_volume=Sum("matic_price"), usdc_volume=Sum("usdc_price"), weth_volume=Sum('weth_price'), total_transactions=Count('id'))

    matic_spot_price = SpotPrice.objects.get(token_name="MATIC").price
    weth_spot_price = SpotPrice.objects.get(token_name="WETH").price
    usdc_spot_price = 1

    monthly_sales_721 = Seaport721Transaction.objects.filter(q).annotate(
        month=TruncMonth('tx_hash__dt'),
    ).values('month').annotate(
        matic_volume=(Sum('matic_price')/(10**18)),
        usdc_volume=(Sum('usdc_price')/(10**6)),
        weth_volume=(Sum('weth_price')/(10**18)),
        total_sales=(Count('id')),
        spot_usd_volume=((Sum('matic_price', output_field=FloatField())/(10**18))*matic_spot_price) + ((Sum('usdc_price', output_field=FloatField())/(10**6))) + ((Sum('weth_price', output_field=FloatField())/(10**18))*weth_spot_price),
        average_sale_price=(((Sum('matic_price', output_field=FloatField())/(10**18))*matic_spot_price) + ((Sum('usdc_price', output_field=FloatField())/(10**6))) + ((Sum('weth_price', output_field=FloatField())/(10**18))*weth_spot_price)) / (Count('id'))
    )

    monthly_sales_1155 = Seaport1155Transaction.objects.filter(q).annotate(
        month=TruncMonth('tx_hash__dt'),
    ).values('month').annotate(
        matic_volume=(Sum('matic_price')/(10**18)),
        usdc_volume=(Sum('usdc_price')/(10**6)),
        weth_volume=(Sum('weth_price')/(10**18)),
        total_sales=(Count('id')),
        total_individual_tokens_sold=Sum("quantity"),
        spot_usd_volume=((Sum('matic_price', output_field=FloatField())/(10**18))*matic_spot_price) + ((Sum('usdc_price', output_field=FloatField())/(10**6))) + ((Sum('weth_price', output_field=FloatField())/(10**18))*weth_spot_price),
        average_sale_price=(((Sum('matic_price', output_field=FloatField())/(10**18))*matic_spot_price) + ((Sum('usdc_price', output_field=FloatField())/(10**6))) + ((Sum('weth_price', output_field=FloatField())/(10**18))*weth_spot_price)) / (Count('id')),
        average_sale_price_per_individual_token=(((Sum('matic_price', output_field=FloatField())/(10**18))*matic_spot_price) + ((Sum('usdc_price', output_field=FloatField())/(10**6))) + ((Sum('weth_price', output_field=FloatField())/(10**18))*weth_spot_price)) / (Sum('quantity', output_field=FloatField()))
    )

    response = {
        "status": "success",
        "data": {
            "721": list(monthly_sales_721),
            "1155": list(monthly_sales_1155)
        },
        "parameters": params
    }

    return JsonResponse(response)