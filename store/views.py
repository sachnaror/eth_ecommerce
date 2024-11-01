import os

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from dotenv import load_dotenv
from web3 import Web3

# Load environment variables
load_dotenv()

# Connect to Ethereum node (e.g., Infura)
infura_url = os.getenv("INFURA_URL")  # Load Infura URL from the .env file
web3 = Web3(Web3.HTTPProvider(infura_url))

# Contract details
contract_address = os.getenv("CONTRACT_ADDRESS")  # Load contract address from the .env file
contract_address = web3.toChecksumAddress(contract_address)  # Convert to checksum address

# ABI for the smart contract
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
        user_account = request.POST.get('account')  # Get the user's account from the request

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

        # Ensure user account address is valid
        if not web3.isAddress(user_account):
            return JsonResponse({'error': 'Invalid user account address.'}, status=400)

        # Interact with the smart contract to create a product
        try:
            tx_hash = contract.functions.createProduct(product_name, web3.toWei(price, 'ether')).transact({'from': user_account})
            receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
            return JsonResponse({'status': 'Product added', 'transaction': receipt.transactionHash.hex()}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method.'}, status=405)

@csrf_exempt
def buy_product(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        user_account = request.POST.get('account')  # Get the user's account from the request

        # Validate product ID and account address
        if not product_id.isdigit():
            return JsonResponse({'error': 'Invalid product ID.'}, status=400)

        if not web3.isAddress(user_account):
            return JsonResponse({'error': 'Invalid user account address.'}, status=400)

        try:
            # Assuming a fixed purchase price for simplicity
            receipt = contract.functions.purchaseProduct(int(product_id)).transact({
                'from': user_account,
                'value': web3.toWei(0.01, 'ether')  # Adjust this value based on your contract's logic
            })
            return JsonResponse({"status": "Purchase complete", "transaction": receipt.transactionHash.hex()})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request method.'}, status=405)

@csrf_exempt
def update_data_view(request):
    if request.method == 'POST':
        value = request.POST.get("value")
        account = request.POST.get("account")  # User's account address (from MetaMask)

        # Validate the value and account address
        if not value.isdigit():
            return JsonResponse({'error': 'Invalid value provided.'}, status=400)

        if not web3.isAddress(account):
            return JsonResponse({'error': 'Invalid user account address.'}, status=400)

        try:
            receipt = set_data(int(value), account)
            return JsonResponse({"status": "Data updated", "transaction": receipt.transactionHash.hex()})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request method.'}, status=405)
