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

    data721 = Seaport1155Transaction.objects.filter(q)
    data1155 = Seaport721Transaction.objects.filter(q)
    
    response = {
        'status': "success",
        "data": list(data721.values()) + list(data1155.values())
    }
    return JsonResponse(response)
    
    

@csrf_exempt
def get_sales_by_contract(request):
    return JsonResponse({})
#     if "contract_address" in request.GET:
#         contract_address = request.GET['contract_address']
#     else:
#         return JsonResponse({'error': "no contract address provided"})
#     if "start_dt" in request.GET:
#         start_dt = request.GET['start_dt']
#     else:
#         start_dt = None
#     if "end_dt" in request.GET:
#         end_dt = request.GET['end_dt']
#     else:
#         end_dt = None
#     seaport_1155_txs = Seaport1155Transaction.objects.filter(
#         contract_address=contract_address
#     )
#     seaport_721_txs = Seaport1155Transaction.objects.filter(
#         contract_address=contract_address
#     )
#     if start_dt:
#         seaport_1155_txs = seaport_1155_txs.filter(start_dt__date="2023-02-23")
#     return JsonResponse({"data":[contract_address, token_id, start_dt, end_dt]})

# @csrf_exempt
# def get_volume_by_token(request):
#     contract_address = request.GET['contract_address']
#     token_id = request.GET['token_id']
#     start_dt = request.GET['start_dt']
#     end_dt = request.GET['end_dt']
#     return JsonResponse({"data":[contract_address, token_id, start_dt, end_dt]})

# @csrf_exempt
# def get_sales_by_token_id(request):
#     contract_address = request.GET['contract_address']
#     token_id = request.GET['token_id']
#     start_dt = request.GET['start_dt']
#     end_dt = request.GET['end_dt']
#     return JsonResponse({"data":[contract_address, token_id, start_dt, end_dt]})

# @csrf_exempt
# def get_volume_by_token_id(request):
#     contract_address = request.GET['contract_address']
#     token_id = request.GET['token_id']
#     start_dt = request.GET['start_dt']
#     end_dt = request.GET['end_dt']
#     return JsonResponse({"data":[contract_address, token_id, start_dt, end_dt]})