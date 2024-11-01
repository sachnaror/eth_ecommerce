from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from web3 import Web3

from .utils import create_product, purchase_product

# Connect to Ethereum node (e.g., Infura)
infura_url = "https://rinkeby.infura.io/v3/YOUR_INFURA_PROJECT_ID"  # Replace with your Infura project ID
web3 = Web3(Web3.HTTPProvider(infura_url))

# Contract details
contract_address = "0x1234567890abcdef1234567890abcdef12345678"  # Replace with your deployed contract address
contract_address = web3.toChecksumAddress(contract_address)  # Convert to checksum address
contract_abi = [
    {
        "inputs": [{"internalType": "string", "name": "name", "type": "string"},
                   {"internalType": "uint256", "name": "price", "type": "uint256"}],
        "name": "createProduct",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "uint256", "name": "productId", "type": "uint256"}],
        "name": "purchaseProduct",
        "outputs": [],
        "stateMutability": "payable",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "getProducts",
        "outputs": [{"internalType": "tuple[]", "name": "", "type": "tuple(uint256,string,uint256)"}],
        "stateMutability": "view",
        "type": "function"
    }
]

# Create contract instance
contract = web3.eth.contract(address=contract_address, abi=contract_abi)


@csrf_exempt
def add_product(request):
    if request.method == 'POST':
        product_name = request.POST.get('name')
        product_price = request.POST.get('price')

        # Validate product name
        if not product_name or len(product_name.strip()) == 0:
            return JsonResponse({'error': 'Invalid product name.'}, status=400)

        # Validate product price
        try:
            price = float(product_price)
            if price <= 0:
                raise ValueError
        except (ValueError, TypeError):
            return JsonResponse({'error': 'Invalid product price.'}, status=400)

        # Interact with the smart contract to create a product
        try:
            # Here, you would need to specify the user's account address from the request
            # You might need to pass the user's account address with your request
            user_account = request.POST.get('account')  # Get the user's account from request
            tx_receipt = contract.functions.createProduct(product_name, web3.toWei(price, 'ether')).transact({'from': user_account})
            return JsonResponse({'status': 'Product added', 'transaction': tx_receipt.hex()}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method.'}, status=405)


@csrf_exempt
def buy_product(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        user_account = request.POST.get('account')  # Get the user's account from request

        try:
            receipt = contract.functions.purchaseProduct(int(product_id)).transact({
                'from': user_account,
                'value': web3.toWei(0.01, 'ether')  # Assuming a fixed purchase price
            })
            return JsonResponse({"status": "Purchase complete", "transaction": receipt.hex()})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request method.'}, status=405)


@csrf_exempt
def update_data_view(request):
    if request.method == 'POST':
        value = request.POST.get("value")
        account = request.POST.get("account")  # User's account address (from MetaMask)

        try:
            receipt = set_data(int(value), account)
            return JsonResponse({"status": "Data updated", "transaction": receipt.transactionHash.hex()})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request method.'}, status=405)
