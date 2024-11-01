import os

from dotenv import load_dotenv
from web3 import Web3

# Load environment variables from .env file
load_dotenv()

# Connect to Ethereum node (e.g., Infura)
infura_url = os.getenv("INFURA_URL")  # Load the Infura URL from the environment variables
web3 = Web3(Web3.HTTPProvider(infura_url))

# Contract details
contract_address = os.getenv("CONTRACT_ADDRESS")  # Load the contract address from the environment variables
contract_address = web3.toChecksumAddress(contract_address)  # Convert to checksum address

# ABI for the Smart Contract (Replace with your actual contract ABI)
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
]

# Create contract instance
contract = web3.eth.contract(address=contract_address, abi=contract_abi)

def set_data(value, account):
    """Set the value in the contract."""
    estimated_gas = contract.functions.set(value).estimateGas({'from': account})
    gas_price = web3.eth.gas_price
    total_cost = estimated_gas * gas_price
    balance = web3.eth.get_balance(account)

    if balance < total_cost:
        raise Exception("Insufficient funds to cover gas fees.")

    tx_hash = contract.functions.set(value).transact({
        'from': account,
        'gas': estimated_gas,
        'gasPrice': gas_price
    })

    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    return receipt

def get_data():
    """Get the value from the contract."""
    return contract.functions.get().call()

def create_product(name, price, account):
    """Function to create a new product on the blockchain."""
    try:
        price_in_wei = web3.toWei(price, 'ether')
        tx_hash = contract.functions.createProduct(name, price_in_wei).transact({'from': account})
        receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        return receipt
    except Exception as e:
        raise Exception(f"Error creating product: {str(e)}")

def purchase_product(product_id, account):
    """Function to purchase a product from the blockchain store."""
    try:
        product_price = web3.toWei(0.01, 'ether')  # Example price in Ether
        tx_hash = contract.functions.purchaseProduct(product_id).transact({
            'from': account,
            'value': product_price
        })
        receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        return receipt
    except Exception as e:
        raise Exception(f"Error purchasing product: {str(e)}")
