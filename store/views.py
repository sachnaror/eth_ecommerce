# Adding views for listing products, adding new ones, and purchasing products.
from django.http import JsonResponse
from web3 import Web3

from .utils import create_product, purchase_product

# Connect to Ethereum node (e.g., Infura)
infura_url = "https://rinkeby.infura.io/v3/YOUR_INFURA_PROJECT_ID"  # Replace with your Infura project ID
web3 = Web3(Web3.HTTPProvider(infura_url))

# Contract details
contract_address = "0x1234567890abcdef1234567890abcdef12345678"  # Using dummy Contract address
contract_address = web3.to_checksum_address(contract_address)  # To Convert to checksum address
 # Replace with your deployed contract address
contract_abi = [
    {
        "inputs": [{"internalType": "uint256", "name": "x", "type": "uint256"}],
        "name": "set",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "get",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "anonymous": False,
        "inputs": [],
        "name": "StoredDataUpdated",
        "type": "event"
    }  # Paste the ABI from your compiled contract here
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

from django.http import JsonResponse

from .utils import get_data, set_data


def update_data_view(request):
    value = request.GET.get("value")
    account = request.GET.get("account")  # User's account address (from MetaMask)

    try:
        receipt = set_data(int(value), account)
        return JsonResponse({"status": "Data updated", "transaction": receipt.transactionHash.hex()})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
