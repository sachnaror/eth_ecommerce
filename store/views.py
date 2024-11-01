//Adding views for listing products, adding new ones, and purchasing products.

from django.http import JsonResponse

from .utils import create_product, purchase_product


def add_product(request):
    name = request.GET.get("name")
    price = int(request.GET.get("price"))
    receipt = create_product(name, price)
    return JsonResponse({"status": "Product added", "transaction": receipt.transactionHash.hex()})

def buy_product(request):
    product_id = int(request.GET.get("product_id"))
    receipt = purchase_product(product_id)
    return JsonResponse({"status": "Purchase complete", "transaction": receipt.transactionHash.hex()})
