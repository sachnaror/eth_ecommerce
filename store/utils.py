from web3 import Web3

# Connect to Ethereum node (e.g., Infura)
infura_url = "https://rinkeby.infura.io/v3/YOUR_INFURA_PROJECT_ID"
web3 = Web3(Web3.HTTPProvider(infura_url))

# Contract details
contract_address = "0x1234567890abcdef1234567890abcdef12345678"  # Your contract address
contract_address = web3.toChecksumAddress(contract_address)  # Convert to checksum address
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
    }
    # Paste your ABI here
]

contract = web3.eth.contract(address=contract_address, abi=contract_abi)

def create_product(name, price):
    """Function to create a new product on the blockchain."""
    tx_hash = contract.functions.createProduct(name, price).transact()
    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    return receipt

def purchase_product(product_id):
    """Function to purchase a product from the blockchain store."""
    tx_hash = contract.functions.purchaseProduct(product_id).transact()
    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    return receipt
