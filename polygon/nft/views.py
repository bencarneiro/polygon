from django.shortcuts import render

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from nft.models import SeaportTransaction, Seaport1155Transaction, Seaport721Transaction

# Create your views here.

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