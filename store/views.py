# Adding views for listing products, adding new ones, and purchasing products.
from django.http import JsonResponse
from web3 import Web3

from .utils import create_product, purchase_product

# Connect to Ethereum node (e.g., Infura)
infura_url = "https://rinkeby.infura.io/v3/YOUR_INFURA_PROJECT_ID"  # Replace with your Infura project ID
web3 = Web3(Web3.HTTPProvider(infura_url))

# Contract details
contract_address = "YOUR_CONTRACT_ADDRESS"  # Replace with your deployed contract address
contract_abi = [
    # Paste the ABI from your compiled contract here
]

# Create contract instance
contract = web3.eth.contract(address=contract_address, abi=contract_abi)

def add_product(request):
    # Get product name and price from the request
    name = request.GET.get("name")
    price = int(request.GET.get("price"))

    # Call the create_product function to interact with the smart contract
    receipt = create_product(name, price)

    # Return a JSON response with the transaction details
    return JsonResponse({"status": "Product added", "transaction": receipt.transactionHash.hex()})

def buy_product(request):
    # Get the product ID from the request
    product_id = int(request.GET.get("product_id"))

    # Call the purchase_product function to interact with the smart contract
    receipt = purchase_product(product_id)

    # Return a JSON response with the transaction details
    return JsonResponse({"status": "Purchase complete", "transaction": receipt.transactionHash.hex()})
